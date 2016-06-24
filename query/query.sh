#!/usr/bin/env bash
#
# ./run_queries.sh &> run_queries.txt

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

['../rules/general_rules'].
[yw_views].



set_prolog_flag(unknown, fail).

%-------------------------------------------------------------------------------
banner( 'YW_Q1',
        'What is the name and description of the workflow implemented by the script?',
        'yw_q1(WorkflowName, Description)').
[user].
:- table yw_q1/2.
yw_q1(WorkflowName, Description) :-
    yw_workflow_script(WorkflowId, WorkflowName, _,_),
    yw_description(program, WorkflowId, _, Description).
end_of_file.
printall(yw_q1(_,_)).
%-------------------------------------------------------------------------------



%-------------------------------------------------------------------------------
banner( 'YW_Q2',
        'What workflow steps comprise the top-level workflow?',
        'yw_q2(StepName, Description)').
[user].
:- table yw_q2/2.
yw_q2(StepName, Description) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_workflow_step(StepId, StepName, WorkflowId, _, _, _),
    yw_description(program, StepId, _, Description).
end_of_file.
printall(yw_q2(_,_)).
%-------------------------------------------------------------------------------



banner( 'YW_Q3',
        'Where is the definition of workflow step AMPLITUDE_SPECTRAL_DENSITY?',
        'yw_q3(SourceFile, StartLine, EndLine)').
[user].
:- table yw_q3/3.
yw_q3(SourceFile, StartLine, EndLine) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_workflow_step(_, 'AMPLITUDE_SPECTRAL_DENSITY', WorkflowId, SourceId, StartLine, EndLine),
    yw_source_file(SourceId, SourceFile).
end_of_file.
printall(yw_q3(_,_,_)).
%-------------------------------------------------------------------------------



%-------------------------------------------------------------------------------
banner( 'YW_Q4',
        'What are the names and descriptions of any outputs of the workflow?',
        'yw_q4(OutputName, Description)').
[user].
:- table yw_q4/2.
yw_q4(OutputName, Description) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_step_output(WorkflowId, _, _, PortId, _,_, OutputName),
    yw_description(port, PortId, _, Description).
end_of_file.
printall(yw_q4(_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_Q5',
        'What data flows from the AMPLITUDE_SPECTRAL_DENSITY workflow step to the WHITENING step?',
        'yw_q5(DataName)').
[user].
:- table yw_q5/1.
yw_q5(DataName) :-
    yw_flow(_, 'AMPLITUDE_SPECTRAL_DENSITY', _, _,  _, DataName, _, _, _, 'WHITENING').
end_of_file.
printall(yw_q5(_)).
%-------------------------------------------------------------------------------



%-------------------------------------------------------------------------------
banner( 'YW_Q6',
        'What outputs from the input fn_H1 ?',
        'yw_q6(fn_H1, DataName)').
[user].
:- table yw_q6/2.
yw_q6(fn_H1, DataName) :-
    yw_flow(_, 'LOAD_DATA', _, _,  _, fn_H1, _, _, _, 'AMPLITUDE_SPECTRAL_DENSITY'),
    yw_flow(_, 'AMPLITUDE_SPECTRAL_DENSITY', _, _,  _, _, _, _, _, 'WHITENING'),
    yw_flow(_, 'WHITENING', _, _,  _, _, _, _, _, 'BANDPASSING'),
    yw_flow(_, 'BANDPASSING', _, _,  _, _, _, _, _, 'SHIFT_FREQUENCY_BANDPASSED'),
    yw_flow(_, 'SHIFT_FREQUENCY_BANDPASSED', _, _,  _, DataName1, _, _, _, 'WAVE_FILE_GENERATOR'),
    yw_step_input( _, 'WAVE_FILE_GENERATOR', _, _, _, _, DataName1),
    yw_step_output( _, 'WAVE_FILE_GENERATOR', _, _, _, _, DataName).
end_of_file.
printall(yw_q6(fn_H1, _)).
%-------------------------------------------------------------------------------




%-------------------------------------------------------------------------------
banner( 'YW_Q7',
        'What outputs from the input fn_H1 ?',
        'ancestor(fn_H1)').


printall(ancestor(fn_H1)).

ancestor(DataName) :-
    parent(DataName, NewDataName),
    ancestor(NewDataName).
end_of_file.

parent(DataName, NewDataName) :-
    yw_step_input(_, ProgramName, _, _, _, _, DataName),
    yw_step_output(_, ProgramName, _, _, _, _, NewDataName)
end_of_file.
%-------------------------------------------------------------------------------
END_XSB_STDIN
