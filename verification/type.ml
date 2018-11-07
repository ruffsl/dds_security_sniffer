type a' nonEmptyList =
  | Node of a'
  | LinkedNode of a' * (a' nonEmptyList)

type evalAction = 
  | ALLOW
  | DENY
  | NONE
  | ERROR

type action = 
  | ALLOW
  | DENY

(* why tagNameVauePair is list of list *)
type tagNameValuePair = (string * string) nonEmptyList

type rawCriteria = 
  | RawCriteria  of string nonEmptyList * string list * tagNameValuePair list

type criteria = rawCriteria nonEmptyList

 (* non-neg *)
type domain = 
  | DomainId of int 
  | DomainRange of int * int 

type rule = 
  | Rule of domain nonEmptyList * bool * criteria list * criteria list * criteria list

type validity =
  | Validity of int of int

type grant = 
  | Grant of string * validity * rule nonEmptyList * action 

type permissions = grant nonEmptyList

type subjectAction =
  | PUBLISH
  | SUBSCRIBE
  | RELAY

type subject =
  | Subject of string * subjectAction * int

