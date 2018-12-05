
(* d m y hr min sec *)
let canonical_format = format_of_string "%d-%d-%d%d%d%d"

(* this is a stub, that doesn't support rearrangment
   and works incorrectly for most of inputs *)
let fmt_of_time p = function
  | 'm' | 'Y' | 'H' | 'M' | 'S' -> 'd'
  | x -> x

let transform_format fmt =
  let p = Array.init 6 ~f:ident in (* stub: identity permutation *)
  let fmt = String.map fmt ~f:(fmt_of_time p) in
  let fmt = Scanf.format_from_string fmt canonical_format in
  p, fmt

let strptime data fmt =
  let (p,fmt) = transform_format fmt in
  let of_parts = rearrange of_parts p in
  Scanf.sscanf data fmt of_parts

let is_leap_year y = ((y mod 4 = 0) && (y mod 100 <> 0)) || (y mod 400 = 0)

let yeardays_months = [| 0; 31; 59; 90; 120; 151; 181; 212; 243; 273; 304; 334; |]

(** Convert from GMT time to Unix seconds! *)
let time_to_float (year: int) (month: int) (day: int) (hour: int) (minute: int) (second: int) : float = 
  if year < 1970 then 0.
  else begin
    let tot_days = ref 0 in
    (* Account for the year part. *)
    for y = 1970 to year - 1 do 
      if (is_leap_year y) then tot_days := !tot_days + 366 else tot_days := !tot_days + 365
    done;
    (* Account for the month part. *)
    tot_days := !tot_days + yeardays_months.(month - 1) + day - 1;
    (* And for leap years. *)
    if (is_leap_year year) && month > 2 then tot_days := !tot_days + 1;
    (float_of_int !tot_days) *. 86400. +. (float_of_int hour) *. 3600. +. 
      (float_of_int minute) *. 60. +. (float_of_int second)
  end

