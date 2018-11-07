let checkCriteria (cri : criteria) (sub : subject) : bool = true

let rec match_domain (domains : domain nonEmptyList) (id : int) : bool = 
  let nodeAndNext = 
    (match domains with 
    | Node(d) -> (d, false, domains)
    | LinkedNode(d, next) -> (d, false, next)) in
  match nodeAndNext with
  | (node, hasNext, next) ->
      let matched = 
        (match node with
        | DomainId(did) -> did == id
        | DomainRange(low, high) -> id >= low && id <= high) in
      if matched then 
        matched
      else
        if hasNext then match_domain next id else false

let rec checkRules (rules : rule) (sub : subject) : evalAction = 
  match sub with
  | Subject(_, act, id) ->
      (match rules with
      | head::res ->
          (match head with 
          | Rule(domains, isAllow, publist, sublist, relaylist) ->
              if match_domain domains id then
                let critList = 
                  (match act with
                  | SubjectAction(PUBLISH) -> publist
                  | SubjectAction(SUBSCRIBE) -> sublist
                  | SubjectAction(RELAY) -> relayList) in
                if checkCriteria critList sub then 
                  if isAllow then evalAction(ALLOW) else evalAction(DENY))
                else checkRules res sub
              else checkRules res sub
      | _ -> evalAction(NONE));;

let evaluate (perm : permissions) (sub : subject) (curr_t : int) : evalAction =
  let nodeAndNext = 
    (match perm with
    | Node(g) -> (g, false, perm)
    | LinkedNode(g, next) -> (g, true, next)) in
  let subName = 
    (match sub with
    | SubJect(name, _, _) -> name) in
  match nodeAndNext with
  | (node, hasNext, next) ->
      let matchedAndValid = 
        (match node with
        | grant(name, validTime, rules, default) ->
            if name != subName then false
            else 
              (match validTime with
              | Validity(low, high) -> curr_t >= low && curr_t <= high)) in
      if matchedAndValid then 
        let qualifier = checkRules rules sub in
        (match qualifier with
        | evalAction(NONE) -> default
        | _ -> qualifier)
      else
        if hasNext then evaluate next sub curr_t else evalAction(ERROR);;

