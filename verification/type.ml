type 'a nonEmptyList =
    | Node of 'a
    | LinkedNode of 'a * ('a nonEmptyList)

type qualifier =
  | ALLOW
  | DENY
  | NONE

type criteria = {
  topics : string nonEmptyList;
  partitions : string list;
  tags : (string * string) list
}

type domain =
  | DomainId of int
  | DomainRange of int * int

type rule = {
  domains : domain nonEmptyList;
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

type permissions = grant nonEmptyList

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
(*
let tmp_criteria = {
  topics=Node("tmpTopic");
  partitions=["a"];
  tags=[("b","c")]
}
let tmp_domain = DomainId(0)
let tmp_validity = {low=0;high=1}
let tmp_rule = {
  domains=Node(tmp_domain);
  qualifier=ALLOW;
  publish=[tmp_criteria];
  subscribe=[];
  relay=[]
}

let tmp_grant = {
  subject_name="tmp";
  validity=tmp_validity;
  rules=[tmp_rule];
  default=DENY
}
let tmp_permission = Node (tmp_grant)
let tmp_subject = {
  subName = "hello";
  action=PUBLISH;
  domainId=1;
  topic="wold";
  partition="a";
  dataTag=("a","b");
  time=1

}
*)
