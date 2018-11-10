let tmp_criteria = {
  topics=["wold"];
  partitions=["a"];
  tags=[("a","b")]
}
let tmp_domain = DomainId(0)
let tmp_validity = {low=0;high=2}
let tmp_rule = {
  domains=[tmp_domain];
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
let tmp_permission = [tmp_grant]
let tmp_subject = {
  subName = "tmp";
  action=PUBLISH;
  domainId=0;
  topic="wold";
  partition="a";
  dataTag=("a","b");
  time=1
}

verify(fun (x:subject) -> evaluate tmp_permission x = ALLOW)


let rec bcheckCriteria (cri : criteria list) (sub : subject) : bool =
    match cri with
    | [] -> false
    | h::t ->
        let match_criteria criteria sub =
                inList criteria.topics sub.topic
            && (sub.dataTag = ("", "") || inList criteria.tags sub.dataTag) in
        match_criteria h sub || bcheckCriteria t sub

let rec bcheckRules (rules : rule list) (sub : subject) : qualifier =
  match rules with
  | [] -> NONE
  | head::tail ->
    let in_domain = match_domain head.domains sub.domainId in
     let matched_criteria =
      let critList =
        (match sub.action with
        | PUBLISH -> head.publish
        | SUBSCRIBE -> head.subscribe
        | RELAY -> head.relay) in
     bcheckCriteria critList sub  in
     if in_domain && matched_criteria then head.qualifier
     else bcheckRules tail sub

let rec bevaluate (perm : permissions) (sub : subject) : qualifier =
  match perm with
  | node::next ->
      let matchedAndValid =
        if node.subject_name <> sub.subName then false
        else sub.time >= node.validity.low && sub.time <= node.validity.high in
      if matchedAndValid then
        let evalRes = bcheckRules node.rules sub in
        (match evalRes with
        | NONE -> node.default
        | _  -> evalRes)
      else
        bevaluate next sub
  | [] -> NONE

  verify(fun (x:subject) -> evaluate tmp_permission x = bevaluate tmp_permission x)
