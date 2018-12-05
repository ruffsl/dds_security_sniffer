from imandra_client import ImandraClient


class ReconAgent(ImandraClient):
    def __init__(self, base_url):
        super().__init__(base_url)
        self._config()

    def _config(self):
        super()._init()
        self._eval(data='#redef true')
        self._eval(data='#use "reachability.ml"')
        self._eval(data='Genpp.eval()')
        self._eval(data='''
let reflect_permission_into_logic name value = Pconfig.(with_mode_assigned ~to_:State.Logic
   Imandra.eval_string (Printf.sprintf "let %s = %s" name @@ Pp.pp_permissions value)) [@@program]
''')

    def instance_reachabile(self, perms_x, perms_y, as_bool=True):
        self._eval(
            data='let perms_x = parse_permission_file "{}" [@@program]'.format(perms_x))
        self._eval(
            data='let perms_y = parse_permission_file "{}" [@@program]'.format(perms_y))
        self._eval(
            data='reflect_permission_into_logic "perms_x" perms_x [@@program]')
        self._eval(
            data='reflect_permission_into_logic "perms_y" perms_y [@@program]')
        return self._instance(
            data='fun x y -> reachable x perms_x y perms_y',
            data_type='src',
            as_bool=as_bool)
