let rec inList l target = 
    match l with
    | [] -> false
    | h::t -> h = target || (inList t target)

let rec inNonEmptyList l target = 
    match l with 
    | Node(n) -> n = target
    | LinkedNode (h, t) -> h = target || (inNonEmptyList t target)


let rec checkCriteria (cri : criteria list) (sub : subject) : bool =
    match cri with
    | [] -> false
    | h::t ->  
        let match_criteria criteria sub = 
            inNonEmptyList criteria.topics sub.topic 
            && inList criteria.partitions sub.partition
            && inList criteria.tags sub.dataTag in
        match_criteria h sub || checkCriteria t sub
        

let rec match_domain (domains : domain nonEmptyList) (id : int) : bool =
  let nodeAndNext =
    (match domains with
    | Node(d) -> (d, false, domains)
    | LinkedNode(d, next) -> (d, false, next)) in
  match nodeAndNext with
  | (node, hasNext, next) ->
      let matched =
        (match node with
        | DomainId(did) -> did = id
        | DomainRange(low, high) -> id >= low && id <= high) in
      matched || (hasNext && (match_domain next id))

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
  let nodeAndNext =
    (match perm with
    | Node(g) -> (g, false, perm)
    | LinkedNode(g, next) -> (g, true, next)) in
  match nodeAndNext with
  | (node, hasNext, next) ->
      let matchedAndValid =
        if node.subject_name <> sub.subName then false
        else sub.time >= node.validity.low && sub.time <= node.validity.high in
      if matchedAndValid then
        let evalRes = checkRules node.rules sub in
        (match evalRes with
        | NONE -> node.default
        | _  -> evalRes)
      else
        if hasNext then evaluate next sub else NONE
