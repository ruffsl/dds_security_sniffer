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

