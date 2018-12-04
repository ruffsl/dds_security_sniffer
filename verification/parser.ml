#require "xml-light"
#require "ISO8601"
open Xml
open ISO8601
#use "type.ml"
#program

exception Wrong_parse of string;;

let parse_PCData dom =
    match dom with
    | Xml.Element (tag_name, attributes, children) ->
            print_endline (Xml.to_string dom);
            raise (Wrong_parse "should not be element")
    | Xml.PCData s -> s;;

let get_PCData_from_elem dom =
    match dom with
    | Xml.Element (tag_name, attributes, children) ->
            (match children with
            | [] -> ""
            | h::t -> parse_PCData h)
    | Xml.PCData s ->
            print_endline (Xml.to_string dom);
            raise (Wrong_parse "should not be Xml.PCData");;

let parse_string_to_time str =
    Z.of_float (ISO8601.Permissive.date str)

let parse_tag_list tag_list =
    match tag_list with
    | k::v::t ->
            ((get_PCData_from_elem k), (get_PCData_from_elem v))
    | _ -> raise (Wrong_parse "should be key value pair");;

let parse_data_tags tag =
    match tag with
    | Xml.Element (tag_name, attributes, children) ->
            parse_tag_list children
    | Xml.PCData s ->
            print_endline (Xml.to_string tag);
            raise (Wrong_parse "should not be Xml.PCData");;

let parse_validity vals =

    match vals with
    | Xml.Element (tag_name, attributes, children) ->
            (match children with
            |not_before::not_after::[] ->
                    {
                        low = parse_string_to_time (get_PCData_from_elem not_before);
                        high = parse_string_to_time (get_PCData_from_elem not_after)
                    }
            | _-> raise (Wrong_parse "not valid Validity"))

    | Xml.PCData s ->
            print_endline (Xml.to_string vals);
            raise (Wrong_parse "should not be Xml.PCData");;

let rec parse_criteria_internal l =
    match l with
    | [] -> ([], [], [])
    | h::t ->
        (match h with
		| Xml.Element (tag_name, attributes, children) ->
                        let topics, partitions, tags = parse_criteria_internal t in
                        if tag_name = "topics"
                                then (List.map get_PCData_from_elem children)@topics, partitions, tags
                        else if tag_name = "partitions"
                                then topics, (List.map get_PCData_from_elem children)@partitions, tags
                        else if tag_name = "data_tags"
                                then topics, partitions, (List.map parse_data_tags children)@tags
                        else raise (Wrong_parse "wrong element inside criteria")
                | Xml.PCData s ->
                raise (Wrong_parse "should not be Xml.PCData"));;

let parse_criteria crt =
    match crt with
    | Xml.Element (tag_name, attributes, children) ->
         let topics, partitions, tags = parse_criteria_internal children in
         {
             topics=topics;
             partitions=partitions;
             tags=tags;
    }
    | Xml.PCData s ->
            print_endline (Xml.to_string crt);
            raise (Wrong_parse "should not be Xml.PCData");;


let parse_domain_range domain =
    match domain with
    | Xml.Element (tag_name, attributes, children) ->
        (match children with
        | [elem] ->
           (match elem with
           | Xml.Element (min_or_max, _, _) ->
             if min_or_max = "min" then DomainRange (Z.of_int (int_of_string (get_PCData_from_elem elem)),  233) (* Max DDS Domain ID *)
             else DomainRange (0, Z.of_int (int_of_string (get_PCData_from_elem elem)))
           | Xml.PCData s -> raise (Wrong_parse "should not be Xml.PCData"))
        | min::max::[] -> DomainRange (Z.of_int (int_of_string (get_PCData_from_elem min)), Z.of_int (int_of_string (get_PCData_from_elem max)))
        | _ ->  raise (Wrong_parse "should not be empty domain"))
    | Xml.PCData s ->
            print_endline (Xml.to_string domain);
            raise (Wrong_parse "should not be Xml.PCData");;


let parse_single_domain domain =
    match domain with
    | Xml.Element (tag_name, attributes, children) ->
            if tag_name = "id" then DomainId (Z.of_int (int_of_string (get_PCData_from_elem domain)))
            else parse_domain_range domain
    | Xml.PCData s ->
            print_endline (Xml.to_string domain);
            raise (Wrong_parse "should not be Xml.PCData");;


let parse_domain_list domainList =
    match domainList with
    | Xml.Element (tag_name, attributes, children) ->
            List.map parse_single_domain children
    | Xml.PCData s ->
            print_endline (Xml.to_string domainList);
            raise (Wrong_parse "should not be Xml.PCData");;

let rec parse_qualifier_list qual_list =
    match qual_list with
    | [] -> ([], [], [])
    | h::t ->
        (match h with
		| Xml.Element (tag_name, attributes, children) ->
                        let pub_list, sub_list, rel_list = parse_qualifier_list t in
                        if tag_name = "publish"
                        then (parse_criteria h)::pub_list, sub_list, rel_list
                        else if tag_name = "subscribe"
                        then pub_list, (parse_criteria h)::sub_list, rel_list
                        else if tag_name = "relay"
                        then pub_list, sub_list, (parse_criteria h)::rel_list
                        else raise (Wrong_parse "wrong criteria")
                | Xml.PCData s -> raise (Wrong_parse "should not be Xml.PCData"));;

let parse_single_rule r =
   match r with
    | Xml.Element (tag_name, attributes, children) ->
            (match children with
            | domainlist::quallist ->
                let pub_list, sub_list, rel_list = parse_qualifier_list quallist in
                {
                    domains = parse_domain_list domainlist;
                    qualifier = if tag_name = "deny_rule" then DENY else ALLOW;
                    publish = pub_list;
                    subscribe = sub_list;
                    relay = rel_list
                }
            | _ -> raise (Wrong_parse "should not be empty"))
    | Xml.PCData s -> raise (Wrong_parse "should not be pcdata");;


let parse_default d =
    let s = get_PCData_from_elem d in
            if s = "ALLOW" then ALLOW
            else DENY;;

let split_at_last li =
    let r = List.rev li in
        (List.rev (List.tl r), List.hd r)

let parse_grant g  =
    match g with
    | Xml.Element (tag, _, children) ->
        (match children with
           | subName::vals::tail ->
                let rls_list, default = split_at_last tail in
                {
                    subject_name = get_PCData_from_elem subName;
                    validity = parse_validity vals;
                    rules = List.map parse_single_rule rls_list;
                    default = parse_default default;
                }
           | _ ->
                   print_endline (Xml.to_string g);
                   raise (Wrong_parse "not a valid grant")
        )

    | Xml.PCData s -> raise (Wrong_parse "should not be Xml.PCData");;

(*must work with permission tag*)
let parse_permission dom =
    match dom with
    | Xml.Element (tag_name, attributes, children) ->
            List.map parse_grant children
    | Xml.PCData s -> raise (Wrong_parse "should not be Xml.PCData");;

let parse_permission_file file  =
    let dom = Xml.parse_file file in
    match dom with
    | Xml.Element (tag_name, attributes, children) ->
            (match children with
            | h::t -> parse_permission h
            | _ -> raise (Wrong_parse "file ill format"))
    | Xml.PCData s -> raise (Wrong_parse "should not be Xml.PCData");;
