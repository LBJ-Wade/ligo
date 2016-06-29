import sqlite3

def MQ1(BlockName):
    '''% MQ1:  Where is the definition of block BLOCKNAME?
    :- table mq1/3.
    mq1(SourceFile, StartLine, EndLine) :-
        program_source(BLOCKNAME, SourceFile, StartLine, EndLine).'''
    query = "SELECT source_path, begin_line, end_line FROM program_source WHERE qualified_program_name = :BlockName;"
    cursor.execute(query, {"BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print 'Source file: {}. Start Line: {}, End Line: {} '.format(r[0], r[1], r[2])

def MQ2():
    ''' MQ2:  What is the name and description of the top-level workflow?
     :- table mq2/2.
    mq2(WorkflowName,Description) :-
    top_workflow(W),
    program(W, _, WorkflowName, _, _),
    program_description(W, Description).'''
    query = """SELECT p.qualified_program_name, d.value 
            FROM modelfacts_program p 
            JOIN top_workflow t 
            ON p.program_id = t.program_id 
            JOIN program_description d
            ON p.program_id = d.program_id;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        print 'WorkflowName: {}. Description: {}'.format(r[0], r[1])

def MQ4():
    '''\
    % MQ4:  What are the names of the programs comprising the top-level workflow?
    :- table mq4/1.
    mq4(ProgramName) :-
        top_workflow(W),
        has_subprogram(W, P),
        program(P, ProgramName, _, _, _).'''
    query = """SELECT p.program_name 
            FROM top_workflow t 
            JOIN modelfacts_has_subprogram hs 
            ON t.program_id = hs.program_id 
            JOIN modelfacts_program p 
            ON p.program_id = hs.subprogram_id;"""
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        print 'SubProgram Name: {}'.format(r[0])


def MQ5():
    '''\
    % MQ5:  What are the names and descriptions of the inputs to the top-level workflow?
    :- table mq5/2.
    mq5(InputPortName,Description) :-
        top_workflow(W),
        has_in_port(W, P),
        port(P, _, InputPortName, _, _, _),
        port_description(P, Description).
    '''
    query = """SELECT p.port_name, pd.value 
            FROM top_workflow t 
            JOIN modelfacts_has_in_port hip 
            ON t.program_id = hip.block_id 
            JOIN modelfacts_port p 
            ON hip.port_id = p.port_id 
            JOIN port_description pd 
            ON p.port_id = pd.port_id;"""
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        print 'InputPortName: {}. Description: {}'.format(r[0], r[1])

def MQ6(BlockName):
    '''% MQ6:  What data is output by program block BlockName?
    :- table mq6/2.
    mq6(DataName,Description) :-
        program(P, _,BlockName, _, _),
        has_out_port(P, OUT),
        port_data(OUT, DataName, _),
        port_description(OUT,Description).'''
    query = """SELECT DISTINCT pdata.data_name, pdes.value 
            FROM modelfacts_program p 
            JOIN modelfacts_has_out_port hop 
            ON p.program_id = hop.block_id 
            JOIN port_data pdata 
            ON hop.port_id = pdata.port_id 
            JOIN port_description pdes 
            ON hop.port_id = pdes.port_id 
            WHERE p.qualified_program_name = :BlockName;"""
    cursor.execute(query, {"BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print 'Data Name: {}. Description: {}'.format(r[0], r[1])

def MQ7(BlockName):
    '''% MQ7: What program blocks provide input directly to BLOCKNAME?
    :- table mq7/1.
    mq7(ProgramName) :-
        program(P1, _, BlockName, _, _),
        has_in_port(P1, IN),
        port_data(IN, _, D),
        port_data(OUT, _, D),
        has_out_port(P2, OUT),
        program(P2, _, ProgramName, _, _).'''
    query = """SELECT DISTINCT p2.qualified_program_name 
            FROM modelfacts_program p1 
            JOIN modelfacts_has_in_port hip 
            ON p1.program_id = hip.block_id 
            JOIN port_data pd1 ON hip.port_id = pd1.port_id 
            JOIN port_data pd2 
            ON pd1.qualified_data_name = pd2.qualified_data_name 
            JOIN modelfacts_has_out_port hop 
            ON hop.port_id = pd2.port_id 
            JOIN modelfacts_program p2 
            ON hop.block_id = p2.program_id
            WHERE p1.qualified_program_name = :BlockName;"""
    cursor.execute(query, {"BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print '{} directly provides input to {}'.format(r[0], BlockName)

def MQ8(DataName):
    '''% MQ8: What programs have input ports that receive data data_name?
    :- table mq8/1.
    mq8(ProgramName) :-
        data(D, _, data_name),
        channel(C, D),
        port_connects_to_channel(IN, C),
        has_in_port(P, IN),
        program(P, _, ProgramName, _, _).'''
    query = """SELECT p.qualified_program_name 
            FROM modelfacts_data d 
            JOIN modelfacts_channel c 
            ON d.data_id = c.data_id 
            JOIN modelfacts_port_connects_to_channel pc 
            ON c.channel_id = pc.channel_id 
            JOIN modelfacts_has_in_port hip 
            ON pc.port_id = hip.port_id 
            JOIN modelfacts_program p 
            ON hip.block_id = p.program_id 
            WHERE d.qualified_data_name = :DataName;
            """
    cursor.execute(query, {"DataName": DataName})
    results = cursor.fetchall()
    for r in results:
        print '{} have input ports that receive {}'.format(r[0], DataName)

def MQ9(DataName):
    '''% MQ9: How many ports read data DataName?
    :- table mq9/1.
    mq9(PortCount) :-
        data(D, _, DataName),
        count(data_in_port(_, D), PortCount).'''
    query = """SELECT COUNT(*) 
            FROM modelfacts_data d 
            JOIN data_in_port dip 
            ON dip.data_id = d.data_id 
            WHERE d.qualified_data_name = :DataName;
            """
    cursor.execute(query, {"DataName": DataName})
    results = cursor.fetchall()
    print '{} ports read data {}'.format(results[0][0], DataName)

def MQ10():
    '''% MQ10: How many data are read by more than 1 port in workflow?
    :- table mq10/1.
    mq10(DataCount) :- 
        program(W, 'simulate_data_collection', _, _, _),
        count(data_in_workflow_read_by_multiple_ports(_, W), DataCount).'''
    query = """SELECT COUNT(*) 
            FROM modelfacts_program p 
            JOIN data_in_workflow_read_by_multiple_ports dmp 
            ON p.program_id = dmp. program_id 
            WHERE p.program_name = 'GRAVITATIONAL_WAVE_DETECTION';
            """
    cursor.execute(query)
    results = cursor.fetchall()
    print '{} data are read by more than port in workflow'.format(results[0][0])

def MQ11():
    '''% MQ11: What program blocks are immediately downstream of calculate_strategy?
:- table mq11/1.
    mq11(DownstreamProgramName) :-
        program(P1, DownstreamProgramName, _, _, _),
        program(P2, _, 'simulate_data_collection.calculate_strategy', _, _),
        program_immediately_downstream(P1, P2).'''
    pass
def data_in_port():
    '''% Port P is an input for data D.
    :- table data_in_port/2.
    data_in_port(P, D) :-
        port_connects_to_channel(P, C),
        channel(C, D),
        has_in_port(_, P).'''
    view = """DROP VIEW IF EXISTS data_in_port;
            CREATE VIEW data_in_port AS
            SELECT pc.port_id, c.data_id 
            FROM modelfacts_port_connects_to_channel pc 
            JOIN modelfacts_channel c 
            ON pc.channel_id = c.channel_id 
            JOIN modelfacts_has_in_port hip 
            ON hip.port_id = pc.port_id; 
    """
    cursor.executescript(view)
    
def data_in_port_count():
    '''data_in_port_count(PortCount, D) :-
    data(D, _, _),
    count(data_in_port(_, D), PortCount).'''    
    view = """DROP VIEW IF EXISTS data_in_port_count;
            CREATE VIEW data_in_port_count AS
            SELECT COUNT(*) AS total, d.data_id 
            FROM modelfacts_data d 
            JOIN data_in_port ON d.data_id = data_in_port.data_id 
            GROUP BY d.data_id;
    """
    cursor.executescript(view)

def data_in_workflow_read_by_multiple_ports():
    '''data_in_workflow_read_by_multiple_ports(D, W) :-
    has_subprogram(W, P),
    has_in_port(P, IN),
    port_connects_to_channel(IN, C),
    channel(C, D),
    data_in_port_count(Count, D),
    Count > 1.'''
    view = """DROP VIEW IF EXISTS data_in_workflow_read_by_multiple_ports;
            CREATE VIEW data_in_workflow_read_by_multiple_ports AS
            SELECT DISTINCT c.data_id, s.program_id 
            FROM modelfacts_has_subprogram s 
            JOIN modelfacts_has_in_port hip 
            ON s.subprogram_id = hip.block_id 
            JOIN modelfacts_port_connects_to_channel pc 
            ON hip.port_id = pc.port_id 
            JOIN modelfacts_channel c 
            ON pc.channel_id = c.data_id 
            JOIN data_in_port_count dipc 
            ON dipc.data_id = c.data_id 
            WHERE dipc.total > 1;

    """
    cursor.executescript(view)
 
     
def port_data():
    '''% Port P reads or writes data D with name N and qualified name QN.
    :- table port_data/3.
    port_data(P, N, QN) :-
        port_connects_to_channel(P, C),
        channel(C, D),
        data(D, N, QN).'''
    view = """DROP VIEW IF EXISTS port_data;
            CREATE VIEW port_data AS
            SELECT DISTINCT pc.port_id, d.data_name, d.qualified_data_name 
            FROM modelfacts_port_connects_to_channel pc 
            JOIN modelfacts_channel c 
            ON pc.channel_id = c.channel_id 
            JOIN modelfacts_data d 
            ON c.data_id = d.data_id;
    """
    cursor.executescript(view)
 
def port_description():
    '''\
    % Port P has description D.
    :- table port_description/2.
    port_description(P,D) :-
        port(P, _, _, _, PA, _),
        annotation_qualifies(DA, PA),
        annotation(DA, _, _, 'desc', _, D).
    '''
    view = """DROP VIEW IF EXISTS port_description;
            CREATE VIEW port_description AS
            SELECT DISTINCT p.port_id, a.value 
            FROM modelfacts_port p 
            JOIN extractfacts_annotation_qualifies aq 
            ON p.port_annotation_id = aq.primary_annotation_id 
            JOIN extractfacts_annotation a 
            ON aq.qualifying_annotation_id = a.annotation_id 
            WHERE a.tag = 'desc' OR a.tag = 'as';"""
    cursor.executescript(view)
 
def program_description():
    '''% Program P has description D.
    :- table program_description/2.
    program_description(P,D) :-
        program(P, _, _, BA, _),
       annotation_qualifies(DA, BA),
       annotation(DA, _, _, 'desc', _, D).'''
    view = """DROP VIEW IF EXISTS program_description;
            CREATE VIEW program_description AS
            SELECT DISTINCT p.program_id, a.value 
            FROM modelfacts_program p
            JOIN extractfacts_annotation_qualifies aq 
            ON p.begin_annotation_id = aq.primary_annotation_id 
            JOIN extractfacts_annotation a 
            ON a.annotation_id = aq.qualifying_annotation_id 
            WHERE a.tag = 'desc';"""
    cursor.executescript(view)

def program_immediately_downstream():
    '''% Program P1 is immediately downstream of Program P2.
    :- table program_immediately_downstream/2.
    program_immediately_downstream(P1, P2) :-
        has_in_port(P1, In),
        port_connects_to_channel(In, C),
        port_connects_to_channel(Out, C),
        has_out_port(P2, Out).'''


def program_source():
    '''% Program with qualified name QN is defined in source file SF from first line F to last line L.
    :- table program_source/4.
    program_source(QN, SF, F, L) :-
        program(_, _, QN, BA, EA),
        annotation(BA, S, F, _, _, _),
        annotation(EA, S, L, _, _, _),
        extract_source(S, SF).'''
    view = """DROP VIEW IF EXISTS program_source;
            CREATE VIEW program_source AS
            SELECT DISTINCT p.qualified_program_name, es.source_path,
            a1.line_number AS begin_line, a2.line_number AS end_line
            FROM modelfacts_program p 
            JOIN extractfacts_annotation a1 
            ON p.begin_annotation_id = a1.annotation_id 
            JOIN extractfacts_annotation a2 
            ON p.end_annotation_id = a2.annotation_id 
            JOIN extractfacts_extract_source es 
            ON es.source_id = a1.source_id 
            AND es.source_id = a2.source_id;"""
    cursor.executescript(view)

def subprogram():
    view = """DROP VIEW IF EXISTS subprogram;
            CREATE VIEW subprogram AS
            SELECT subprogram_id
            FROM modelfacts_has_subprogram WHERE EXISTS
               (SELECT a.program_id, b.program_id
               FROM modelfacts_program a JOIN modelfacts_program b);"""
    cursor.executescript(view)
  
def top_workflow():
    ''' % Workflow W is the top-level workflow.
     :- table top_workflow/1.
     top_workflow(W) :-
         workflow(W),
         not subprogram(W).'''
    view = """DROP VIEW IF EXISTS top_workflow;
            CREATE VIEW top_workflow AS
            SELECT program_id 
            FROM modelfacts_workflow
            WHERE program_id NOT IN subprogram;"""
    cursor.executescript(view)

def run_rules():
    subprogram()
    top_workflow()
    program_description()
    port_description()
    program_source()
    port_data()
    data_in_port()
    data_in_port_count()
    data_in_workflow_read_by_multiple_ports()

if __name__ == '__main__':
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    run_rules()
    print "MQ1:  Where is the definition of block GRAVITATIONAL_WAVE_DETECTION.SPECTROGRAMS?"
    BlockName = "GRAVITATIONAL_WAVE_DETECTION.SPECTROGRAMS"
    MQ1(BlockName)
    print "MQ2:  What is the name and description of the top-level workflow?"
    MQ2()
    print "MQ4:  What are the names of the programs comprising the top-level workflow?"
    MQ4()
    print "MQ5:  What are the names and descriptions of the inputs to the top-level workflow?"
    MQ5()
    print "MQ6:  What data is output by program block GRAVITATIONAL_WAVE_DETECTION.SPECTROGRAMS?"
    MQ6(BlockName)
    print "MQ7: What program blocks provide input directly to GRAVITATIONAL_WAVE_DETECTION.SPECTROGRAMS?"
    MQ7(BlockName)
    DataName = "GRAVITATIONAL_WAVE_DETECTION[strain_H1_whitenbp]"
    print "MQ8: What programs have input ports that receive data 'strain_H1_whitenbp'?"
    MQ8(DataName)
    print "MQ9: How many ports read data 'strain_H1_whitenbp'?"
    MQ9(DataName)
    print "MQ10: How many data are read by more than 1 port in workflow?"
    MQ10()
    cursor.close()
    connection.close()

