type qualifier =
  | ALLOW
  | DENY
  | NONE

type criteria = {
  topics : string list;
  partitions : string list;
  tags : (string * string) list
}

type domain =
  | DomainId of int
  | DomainRange of int * int

type rule = {
  domains : domain list;
  qualifier : qualifier;
  publish : criteria list;
  subscribe : criteria list;
  relay : criteria list
}

type validity = {
  low : int;
  high : int;
}

type grant = {
    subject_name : string;
    validity : validity;
    rules : rule list;
    default : qualifier
}

type permissions = grant list

let isValidCriterion c = (List.length c.topics) > 0

let rec isValidCriteria crit =
        match crit with
        | h::t -> (isValidCriterion h) && (isValidCriteria t)
        | [] -> true

let isValidDomain d =
        match d with
        | DomainId(a) -> a >= 0
        | DomainRange(a, b) -> a >= 0 && b > a

let rec isValidDomains ds =
        match ds with
        | h::t -> (isValidDomain h) && (isValidDomains t)
        | [h] -> (isValidDomain h)
        | [] -> false

let isValidRule r =
        (isValidDomains r.domains) && (isValidCriteria r.publish) && (isValidCriteria r.subscribe) && (isValidCriteria r.relay)

let rec isValidRules rules =
        match rules with
        | h::t -> (isValidRule h) && (isValidRules t)
        | [h] -> (isValidRule h)
        | [] -> false

let isValidValidity v = v.low >= 0 && v.low < v.high

let isValidGrant g =
        (g.subject_name <> "") && (isValidValidity g.validity) && (isValidRules g.rules)


let rec isValidPermission p =
        match p with
        | [] -> false
        | [h] -> isValidGrant h
        | h::t -> (isValidGrant h) && (isValidPermission t)



let isValid x =
        match x with
        | hd::xs -> (isValid hd) && (isValid xs)
        | [only] -> isValid only
        | [] -> false
        | {subject_name=_; validity = v; rules = r; default=_} -> (isValid v) && (isValid r)
        | {low=lo; high=hi} -> lo >= 0 && hi >= 0 && lo <= hi
        | {domains=ds; qualifier=_; publish=p; subscribe=s; relay=r} ->
                        (isValid ds) && (List.length p = 0 || isValid p) && (List.length s = 0 || isValid s) && (List.length r = 0 || isValid r)
        | {topics=t; partitions=_;tags=_} -> isValid t
        | "" -> false
        | _ -> true



type subjectAction =
  | PUBLISH
  | SUBSCRIBE
  | RELAY

type subject = {
  subName : string;
  action : subjectAction;
  domainId : int;
  topic : string;
  partition : string;
  dataTag : (string * string);
  time : int
}
