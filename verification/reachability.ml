#use "evaluate.ml"
#logic

let reachable (x:subject) (perms_x: permissions) (y:subject) (perms_y: permissions) bool =
    let x_allowed = (evaluate perms_x x = ALLOW) in
    let y_allowed = (evaluate perms_y y = ALLOW) in

    let common_domain = (x.domainId = y.domainId) in
    let common_topic = (x.topic = y.topic) in
    let common_partition = (x.partition = y.partition) in
    let common_dataTag = (x.dataTag = y.dataTag) in
    let complementary_action = (x.action <> y.action) in
    let qos_match = common_domain
        && common_topic
        && common_partition
        && common_dataTag
        && complementary_action in

    let coincide_time = (x.time = y.time) in

    x_allowed && y_allowed && coincide_time && qos_match
[@@logic];;
