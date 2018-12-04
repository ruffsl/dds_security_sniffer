#use "evaluate.ml"
#use "parser.ml"

let perms_x =
[{subject_name = "CN=talker"; validity = {low = 1382745600; high = 1698360330};
  rules =
   [{domains = [DomainRange (0, 42)]; qualifier = ALLOW;
     publish = [{topics = ["rt/chatter/*"]; partitions = [""]; tags = []}];
     subscribe = []; relay = []}];
  default = DENY}]
  ;;

let perms_y =
[{subject_name = "CN=listener";
  validity = {low = 1382745600; high = 1698360330};
  rules =
   [{domains = [DomainRange (0, 42)]; qualifier = ALLOW; publish = [];
     subscribe = [{topics = ["rt/spam"]; partitions = [""]; tags = []}];
     relay = []}];
  default = DENY}]
  ;;

let test (x:subject) (y:subject) bool =
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
;;
instance test

let perms_y =
[{subject_name = "CN=listener";
  validity = {low = 1382745600; high = 1698360330};
  rules =
   [{domains = [DomainRange (0, 42)]; qualifier = ALLOW; publish = [];
     subscribe = [{topics = ["rt/chatter/foo"]; partitions = [""]; tags = []}];
     relay = []}];
  default = DENY}]
  ;;

let test (x:subject) (y:subject) bool =
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
;;
instance test
