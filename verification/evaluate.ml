#use "parser.ml"
#use "fnmatch.ml"
#logic

let rec inList l target =
    match l with
    | [] -> false
    | h::t -> h = target || (inList t target)

let rec inListFnmatch l target =
    match l with
    | [] -> false
    | h::t -> (fnmatch h target) || (inListFnmatch t target)


let rec checkCriteria (cri : criteria list) (sub : subject) : bool =
    match cri with
    | [] -> false
    | h::t ->
        let match_criteria criteria sub =
                inListFnmatch criteria.topics sub.topic
            && (sub.partition = "" || inListFnmatch criteria.partitions sub.partition)
            && (sub.dataTag = ("", "") || inList criteria.tags sub.dataTag) in
        match_criteria h sub || checkCriteria t sub


let rec match_domain (domains : domain list) (id : int) : bool =
        let checkRange x =
                (match x with
                | DomainId(did) -> did = id
                | DomainRange(low, high) -> id >= low && id <= high) in
        match domains with
        | h::t -> (checkRange h) || (match_domain t id)
        | [] -> false

let rec checkRules (rules : rule list) (sub : subject) : qualifier =
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
     checkCriteria critList sub  in
     if in_domain && matched_criteria then head.qualifier
     else checkRules tail sub

let rec evaluate (perm : permissions) (sub : subject) : qualifier =
  match perm with
  | node::next ->
      let matchedAndValid =
        if node.subject_name <> sub.subName then false
        else sub.time >= node.validity.low && sub.time <= node.validity.high in
      if matchedAndValid then
        let evalRes = checkRules node.rules sub in
        (match evalRes with
        | NONE -> node.default
        | _  -> evalRes)
      else
        evaluate next sub
  | [] -> NONE
