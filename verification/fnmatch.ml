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


let rec fnmatch (matchPattern: string list) (matchString:string list) : bool =
    let l = (matchPattern, matchString) in
    match l with 
    | (a::x, b::y) ->
        (match a with 
        | "[" -> 
            let charsRestAndNot = bracket x in
            (match charsRestAndNot with
            | (chars, x_new, isNot) -> (matchLotsOfChar chars b isNot) && (fnmatch x y)) 
        | "*" -> true
            (*fnmatch matchPattern y || fnmatch x matchString*)
        | "?" -> fnmatch x y
        | _ -> (a = b) && (fnmatch x y))
    | ([], []) -> true
    | _ -> false
    
;;
