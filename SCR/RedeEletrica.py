import pandapower as pp

class ModeloRedeEletrica():

    def __init__(self) -> None:
          
          self.net = pp.create_empty_network()
      

    def DBAR(self, data_DBAR):
          
        self.input_DBAR = data_DBAR

        self.b1 = pp.create_bus(self.net, vn_kv=1.)
        self.b2 = pp.create_bus(self.net, vn_kv=1.)
        self.b3 = pp.create_bus(self.net, vn_kv=1.)
        self.b4 = pp.create_bus(self.net, vn_kv=1.)

        pp.create_ext_grid(self.net, bus=self.b1) # para definir barra slack

    def DLIN(self, data_DLIN) -> None:
           
        self.input_DLIN = data_DLIN

        pp.create_line_from_parameters(self.net, from_bus=self.b1, to_bus=self.b2, length_km=1, r_ohm_per_km = 1.058, x_ohm_per_km = .529, c_nf_per_km = 0., max_i_ka = 100.)
        pp.create_line_from_parameters(self.net, from_bus=self.b2, to_bus=self.b3, length_km=1, r_ohm_per_km = 1.058, x_ohm_per_km = .529, c_nf_per_km = 0., max_i_ka = 100.)
        pp.create_line_from_parameters(self.net, from_bus=self.b2, to_bus=self.b4, length_km=1, r_ohm_per_km = 1.058, x_ohm_per_km = .529, c_nf_per_km = 0., max_i_ka = 100.)

    def DGER(self, data_DGER) -> None:

        self.input_DGER = data_DGER       
        pp.create_gen(self.net,self.b3, p_mw=0.02, vm_pu=0.98)
        pp.create_gen(self.net,self.b4, p_mw=0.01, vm_pu=1.01)
  
    def DLOAD(self, data_DLOAD) -> None:

        self.input_DGER = data_DLOAD      
        pp.create_load(self.net, bus=self.b2, p_mw=0.02, q_mvar=0.02) # definir carga da barra 2
        pp.create_load(self.net, bus=self.b3, p_mw=0.01) # definir carga da barra 3
  