#!/usr/bin/env bash
#
# ./run_queries.sh &> run_queries.txt

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

['../rules/general_rules'].
[yw_views].



set_prolog_flag(unknown, fail).

%-------------------------------------------------------------------------------
banner( 'YW_Q1',
        'Where is the definition of block SPECTROGRAMS_1 and SPECTROGRAMS_2?',
        'yw_q1(WorkflowName, Description)').
[user].
:- table yw_q1/3.
yw_q1(ProgramName, BeginLine, EndLine) :-
    yw_program(_, ProgramName, _, _, BeginLine, EndLine).
end_of_file.

printall(yw_q1('SPECTROGRAMS_1', _, _)).
printall(yw_q1('SPECTROGRAMS_2', _, _)).
%-------


%-------------------------------------------------------------------------------
banner( 'YW_Q2',
        'What is the name and description of the workflow implemented by the script?',
        'yw_q2(WorkflowName, Description)').
[user].
:- table yw_q2/2.
yw_q2(WorkflowName, Description) :-
    yw_workflow_script(WorkflowId, WorkflowName, _,_),
    yw_description(program, WorkflowId, _, Description).
end_of_file.
printall(yw_q2(_,_)).
%-------------------------------------------------------------------------------



%-------------------------------------------------------------------------------
banner( 'YW_Q3',
        'What workflow steps comprise the top-level workflow?',
        'yw_q2(StepName, Description)').
[user].
:- table yw_q3/2.
yw_q3(StepName, Description) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_workflow_step(StepId, StepName, WorkflowId, _, _, _),
    yw_description(program, StepId, _, Description).
end_of_file.
printall(yw_q3(_,_)).
%-------------------------------------------------------------------------------



banner( 'YW_Q4',
        'Where is the definition of workflow step AMPLITUDE_SPECTRAL_DENSITY?',
        'yw_q4(SourceFile, StartLine, EndLine)').
[user].
:- table yw_q4/3.
yw_q4(SourceFile, StartLine, EndLine) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_workflow_step(_, 'AMPLITUDE_SPECTRAL_DENSITY', WorkflowId, SourceId, StartLine, EndLine),
    yw_source_file(SourceId, SourceFile).
end_of_file.
printall(yw_q4(_,_,_)).
%-------------------------------------------------------------------------------



%-------------------------------------------------------------------------------
banner( 'YW_Q5',
        'What are the names and descriptions of any outputs of the workflow?',
        'yw_q4(OutputName, Description)').
[user].
:- table yw_q5/2.
yw_q5(OutputName, Description) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_step_output(WorkflowId, _, _, PortId, _,_, OutputName),
    yw_description(port, PortId, _, Description).
end_of_file.
printall(yw_q5(_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_Q6',
        'What data flows from the AMPLITUDE_SPECTRAL_DENSITY workflow step to the WHITENING step?',
        'yw_q6(DataName)').
[user].
:- table yw_q6/1.
yw_q6(DataName) :-
    yw_flow(_, 'AMPLITUDE_SPECTRAL_DENSITY', _, _,  _, DataName, _, _, _, 'WHITENING').
end_of_file.
printall(yw_q6(_)).
%-------------------------------------------------------------------------------



%-------------------------------------------------------------------------------
banner( 'YW_Q7',
        'What outputs from the input FN_H1 ?',
        'parent(FN_H1, NewDataName)').

[user].
:- table yw_q7/2.
yw_q7(DataName, NewDataName) :-
    yw_step_input(_, ProgramName, _, _, _, _, DataName),
    yw_step_output(_, ProgramName, _, _, _, _, NewDataName).
end_of_file.


printall(yw_q7('FN_H1', _)).
%-------------------------------------------------------------------------------




%-------------------------------------------------------------------------------
banner( 'YW_Q8',
        'What outputs from the input FN_H1?',
        'parent(FN_H1, NewDataName)').

[user].
:- table ancestor/1.
ancestor(DataName) :-
    parent(DataName, NewDataName),
    ancestor(NewDataName).
end_of_file.

:- table parent/2.
parent(DataName, NewDataName) :-
    yw_step_input(_, ProgramName, _, _, _, _, DataName),
    yw_step_output(_, ProgramName, _, _, _, _, NewDataName).


printall(ancestor(_)).

%-------------------------------------------------------------------------------



%-------------------------------------------------------------------------------
banner( 'YW_Q9',
        'What inputs from the output GW150914_H1_whitenbp.wav ?',
        'yw_q9(DataNameIn, GW150914_H1_whitenbp.wav)').

[user].
:- table yw_q9/2.
yw_q9(DataNameIn, DataNameOut) :-
    yw_step_output(_, ProgramName, _, _, _, _, DataNameOut),
    yw_step_input(_, ProgramName, _, _, _, _, DataNameIn).
end_of_file.


printall(yw_q9(_, 'GW150914_H1_whitenbp.wav')).
%-------------------------------------------------------------------------------



%-------------------------------------------------------------------------------
banner( 'YW_1Q',
        'What programs have input ports that receive data strain_H1_whitenbp ?',
        'yw_q10(DataNameIn, GW150914_H1_whitenbp.wav)').

[user].
:- table yw_q10/2.
yw_q10(DataNameIn, ProgramName) :-
    yw_step_input(_, ProgramName, _, _, _, _, DataNameIn).
end_of_file.


printall(yw_q10('strain_H1_whitenbp', _)).
%-------------------------------------------------------------------------------




END_XSB_STDIN
