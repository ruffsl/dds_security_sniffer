let rec recbracket x =
    match x with 
    | [] -> ([], [])
    | "]"::res -> ([], res)
    | a::res -> 
        let charsRestAndNot = recbracket res in
            (match charsRestAndNot with
            | (chars, x_new) -> (a::chars, x_new))

let bracket x =
    match x with
    | [] -> ([],[],false)
    | "!"::res -> 
        (match (recbracket res) with
        | (chars, x_new) -> (chars, x_new, true))
    | _::res -> 
        (match (recbracket res) with
        | (chars, x_new) -> (chars, x_new, false))
        
let rec matchLotsOfChar (chars : string list) (char: string) (isNot: bool) : bool =
    match chars with
    | [] -> isNot
    | hd::rs -> 
        if isNot then
            if (hd = char) then false else matchLotsOfChar rs char isNot
        else
            if (hd = char) then true else matchLotsOfChar rs char isNot 

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

let rec fnmatch (matchPattern: string list) (matchString:string list) : bool =
    let l = (matchPattern, matchString) in
    match l with 
    | (a::x, b::y) ->
        (match a with 
        | "[" -> 
            let charsRestAndNot = bracket x in
            (match charsRestAndNot with
            | (chars, x_new, isNot) -> (matchLotsOfChar chars b isNot) && (fnmatch x y)) 
        | "*" ->
                 fnmatch x matchString
        | "?" -> fnmatch x y
        | _ -> (a = b) && (fnmatch x y))
    | ([], []) -> true
    | ([], _) -> false
    | (_, [])  -> false   
;;
