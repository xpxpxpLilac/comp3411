%Student: Yuexuan Liu
%zID: z5093599
%Prolog programming

%Questiton 1
%sumsq_even(Numbers, Sum)
%Given a list, 
% sums the squares of only the even numbers in a list of integers.

sumsq_even([], 0).
sumsq_even([Head | Rest], Sum) :-
	0 is Head mod 2,
	Square is Head * Head,
	sumsq_even(Rest, RestSum), 
	Sum is RestSum + Square.
sumsq_even([Head | Rest], Sum) :-
	not(0 is Head mod 2),
        sumsq_even(Rest, Sum).




% Question2
%
%has_father(Person, Father)
% succeeds when a Person has father
%
has_father(Person, Father) :-
        parent(Father, Person),
        male(Father).

%old_ancestor(Person, Ancestor)
% succeeds when Ancestor is the oldest ancestor of Person
%
old_ancestor(Person, Person) :-
        not(has_father(Person, _Father)),
	male(Person).
old_ancestor(Person, Ancestor) :-
        has_father(Person, Ancestor),
        not(has_father(Ancestor, _Father)).
old_ancestor(Person, Ancestor) :-
        has_father(Person, Father),
        old_ancestor(Father, Ancestor).

%same_name(Person1,Person2)
%
same_name(Person,Person).
same_name(Person1, Person2) :-
        old_ancestor(Person1, Ancestor),
        old_ancestor(Person2, Ancestor).



% Question3
%sqrt_list(NumberList, ResultList)
sqrt_list([], []).
sqrt_list([Head | Rest], [[Head, Sqrt] | RestResult]) :-
	Sqrt is sqrt(Head),
	sqrt_list(Rest, RestResult).


% Question4
%find_list(list, resultList, restList)
find_list([], [], []).
find_list([H], [H], []).
find_list([Item1,Item2 | Rest], [Item1], [Item2 | Rest]) :-
	Multiple is (Item1+0.5) * (Item2+0.5),
	Multiple =< 0.
find_list([Item1,Item2 | Rest],[Item1 | RestResultList], RestList) :-
	Multiple is (Item1+0.5) * (Item2+0.5),
        Multiple > 0,
	find_list([Item2 | Rest], RestResultList, RestList).

%sign_runs(List,patitionList)	
sign_runs([], []).
sign_runs(List, [ResultList | RestResultList]) :-
	List \= [],
	find_list(List, ResultList, RestList),
	sign_runs(RestList, RestResultList).



% Question5
% is_heap(Tree) which returns 
% true if Tree satisfies the heap property
% false otherwise.

is_heap(tree(empty,_N,empty)).
is_heap(tree(tree(empty,N1,empty), N2, tree(empty,N3,empty))):-
        N2 =< N1,
        N2 =< N3.
is_heap(tree(tree(L1,N1,R1), N2, empty)):-
        is_heap(tree(L1,N1,R1)),
        N2 =< N1.
is_heap(tree(empty, N2, tree(L3,N3,R3))):-
        is_heap(tree(L3,N3,R3)),
        N2 =< N3.
is_heap(tree(tree(L1,N1,R1),N2,tree(L3,N3,R3))):-
        N2 =< N1,
        N2 =< N3,
	is_heap(tree(L1,N1,R1)),
        is_heap(tree(L3,N3,R3)).

