same_symbol(A,B):-
    A >= 0,
    B >= 0. 
same_symbol(A,B):-
    A < 0,
    B < 0. 
find_list([],[],[]). 
find_list([Head],[Head],[]). 
find_list([First,Second|Rest],[First],[Second|Rest]):-
    \+same_symbol(First,Second). 
find_list([First,Second | Rest],[First | RestResultList], RestList):-
    same_symbol(First,Second),
    find_list([Second | Rest], RestResultList, RestList). 
sign_runs([],[]). 
sign_runs(List,[ResultList|RestResultList]):-
    List \= [],
    find_list(List,ResultList,RestList),
    sign_runs(RestList,RestResultList).
