let checkCriteria (cri : criteria list) (sub : subject) : bool = true

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

let rec checkRules (rules : rule list) (sub : subject) : evalResult =
  match rules with
  | head::res ->
    if match_domain head.domains sub.domainId then
      let critList =
        (match sub.action with
        | PUBLISH -> head.publish
        | SUBSCRIBE -> head.subscribe
        | RELAY -> head.relay) in
      if checkCriteria critList sub then
        (if head.qualifier = ALLOW then ALLOWED else DENIED)
      else checkRules res sub
    else checkRules res sub
  | _ -> NONE

let evaluate (perm : permissions) (sub : subject) : evalResult =
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
        let evalRes = checkRules rules sub in
        (match evalRes with
        | NONE -> default
        | _ -> qualifier)
      else
        if hasNext then evaluate next sub curr_t else ERROR
