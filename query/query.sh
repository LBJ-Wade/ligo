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


END_XSB_STDIN
