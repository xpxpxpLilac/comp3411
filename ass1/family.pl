% Program:  family.pl
% Source:   Prolog
%
% Purpose:  This is the sample program for the Prolog Lab in COMP9414/9814/3411.
%           It is a simple Prolog program to demonstrate how prolog works.
%           See lab.html for a full description.
%
% History:  Original code by Barry Drake


% parent(Parent, Child)
%
parent(albert, jim).
parent(albert, peter).
parent(jim, brian).
parent(john, darren).
parent(peter, lee).
parent(peter, sandra).
parent(peter, james).
parent(peter, kate).
parent(peter, kyle).
parent(brian, jenny).
parent(irene, jim).
parent(irene, peter).
parent(pat, brian).
parent(pat, darren).
parent(amanda, jenny).


% female(Person)
%
female(irene).
female(pat).
female(lee).
female(sandra).
female(jenny).
female(amanda).
female(kate).

% male(Person)
%
male(albert).
male(jim).
male(peter).
male(brian).
male(john).
male(darren).
male(james).
male(kyle).


% yearOfBirth(Person, Year).
%
yearOfBirth(irene, 1923).
yearOfBirth(pat, 1954).
yearOfBirth(lee, 1970).
yearOfBirth(sandra, 1973).
yearOfBirth(jenny, 2004).
yearOfBirth(amanda, 1979).
yearOfBirth(albert, 1926).
yearOfBirth(jim, 1949).
yearOfBirth(peter, 1945).
yearOfBirth(brian, 1974).
yearOfBirth(john, 1955).
yearOfBirth(darren, 1976).
yearOfBirth(james, 1969).
yearOfBirth(kate, 1975).
yearOfBirth(kyle, 1976).

descendant(Person, Descendant) :-
        parent(Person, Descendant).
descendant(Person, Descendant) :-
        parent(Person, Child),
        descendant(Child, Descendant).


ancestor(Person, Ancestor) :-
        male(Ancestor),
        parent(Ancestor, Person).
ancestor(Person, Ancestor) :-
        parent(Parent, Person),
        male(Parent),
        ancestor(Parent, Ancestor).

has_father(Person, Father) :-
	parent(Father, Person),
	male(Father).
old_ancestor(Person, Ancestor) :-
	has_father(Person, Ancestor),
	not(has_father(Ancestor, _Father)).
old_ancestor(Person, Ancestor) :-
	has_father(Person, Father),
	old_ancestor(Father, Ancestor).
same_name(Person1, Person2) :-
	old_ancestor(Person1, Ancestor),
        old_ancestor(Person2, Ancestor).
	
