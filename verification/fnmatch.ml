let explode s =
  let rec exp subs l =
    if String.length subs = 0 then l
    else
        let elem = String.sub subs 0 1 in
        let e = match elem with Some el -> el | None -> "" in
        let subsub = String.sub subs 1 ((String.length subs) - 1) in
        match subsub with
        | Some s ->
            let tail = exp s l in
            e::tail
        | None -> e::l
    in
      exp s []

let rec _fnmatch (matchPattern:string list) (matchString:string list) : bool =
    match (matchPattern, matchString) with
    | (a::x, b::y) ->
        (match a with
        | "*" ->
            (match x with
            | [] -> true
            | _ -> false)
        | _ -> (a = b) && (_fnmatch x y))
    | ([], []) -> true
    | _ -> false

let fnmatch (matchPattern:string) (matchString:string) : bool =
    _fnmatch (explode matchPattern) (explode matchString)
;;
