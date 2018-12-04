#logic

let fnmatch (matchPattern:string) (matchString:string) : bool =
    if String.suffix "*" matchPattern then
        let index = (String.length matchPattern) - 1 in
        let prefix = (String.sub matchPattern 0 index) in
        match prefix with
        | Some pre -> String.prefix pre matchString
        | None -> true
    else
        matchPattern = matchString
