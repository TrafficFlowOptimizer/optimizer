int: n_students;
int: n_faculties_total;

set of int: Student = 1..n_students;
set of int: Faculty = 1..n_faculties_total;

array[Faculty] of 0..1: faculties_available;
array[Faculty] of int: faculties_sizes;
array[Student] of 0..infinity: student_faculties_no;
array[Student, Faculty] of Faculty: student_prefers;
array[Student] of 0..1: prepared_students;


array[Student, Faculty] of var bool: student_gets;

%nieaktywne obieraki
constraint forall(F in Faculty where faculties_available[F]=0)(sum(S in Student)(student_gets[S,F])=0);

%ilosc obieraków zaspokojona
constraint forall(S in Student)(sum(F in Faculty)(student_gets[S,F])=student_faculties_no[S]);

%brak przeładowania możliwych slotów z przedmiotów
constraint forall(F in Faculty)(sum(S in Student)(student_gets[S,F])<=faculties_sizes[F]*14);

%przygotowanie do obrazów
constraint forall(S in Student)(student_gets[S,4]<=prepared_students[S]);

var 0..10000 : objective = sum([student_gets[S, F]*student_prefers[S, F] | F in Faculty, S in Student]);
solve maximize objective;


% solve satisfy;

output [show(S) ++ " " ++
join(" ", [show(F) | F in Faculty where fix(student_gets[S, F])])
++ "\n" | S in Student]
++ ["\n" ++ show(objective) ++ "\n"];