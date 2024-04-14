import pandapower as pp

class SistemaTeste_4Barras():

    def __init__(self) -> None:
          
          self.net = pp.create_empty_network()
          
          self.DBAR = self.DBAR()
          self.DLIN = self.DLIN()
          self.DGER = self.DGER()
          self.DLOAD = self.DLOAD()
      

    def DBAR(self) -> None:
        
        self.b1 = pp.create_bus(self.net, vn_kv=1.)
        self.b2 = pp.create_bus(self.net, vn_kv=1. , min_vm_pu=0.95,max_vm_pu=1.05)
        self.b3 = pp.create_bus(self.net, vn_kv=1.)
        self.b4 = pp.create_bus(self.net, vn_kv=1.)

        pp.create_ext_grid(self.net, bus=self.b1) # para definir barra slack

    def DLIN(self) -> None:

        self.l1 = pp.create_line_from_parameters(self.net, from_bus=self.b1, to_bus=self.b2, length_km=1, r_ohm_per_km = 1.058, x_ohm_per_km = .529, c_nf_per_km = 0., max_i_ka = 100.)
        self.l2 = pp.create_line_from_parameters(self.net, from_bus=self.b2, to_bus=self.b3, length_km=1, r_ohm_per_km = 1.058, x_ohm_per_km = .529, c_nf_per_km = 0., max_i_ka = 100.)
        self.l3 = pp.create_line_from_parameters(self.net, from_bus=self.b2, to_bus=self.b4, length_km=1, r_ohm_per_km = 1.058, x_ohm_per_km = .529, c_nf_per_km = 0., max_i_ka = 100.)

    def DGER(self) -> None:

        pp.create_gen(self.net,self.b3, p_mw=0.02, vm_pu=0.98)
        pp.create_gen(self.net,self.b4, p_mw=0.01, vm_pu=1.01)
  
    def DLOAD(self) -> None:
        
        pp.create_load(self.net, bus=self.b2, p_mw=0.02, q_mvar=0.02) # definir carga da barra 2
        pp.create_load(self.net, bus=self.b3, p_mw=0.01) # definir carga da barra 3
      
    def DMED(self) -> None:

        pp.create_measurement(self.net,"v","bus",1.001*self.net.res_bus.vm_pu[0], 0.004, self.b1)
        pp.create_measurement(self.net,"p","bus",1.001*self.net.res_bus.p_mw[1], 0.004, self.b2)
        pp.create_measurement(self.net,"p","bus",1.001*self.net.res_bus.p_mw[2], 0.004, self.b3)
        pp.create_measurement(self.net,"p","bus",1.001*self.net.res_bus.p_mw[3], 0.004, self.b4)

        pp.create_measurement(self.net,"v","bus",1.001*self.net.res_bus.vm_pu[1], 0.004, self.b2)
        pp.create_measurement(self.net,"q","bus",1.001*self.net.res_bus.q_mvar[1], 0.004, self.b2)
        pp.create_measurement(self.net,"q","bus",1.001*self.net.res_bus.q_mvar[2], 0.004, self.b3)
        pp.create_measurement(self.net,"q","bus",1.001*self.net.res_bus.q_mvar[3], 0.004, self.b4)

        pp.create_measurement(self.net,"p","line",1.001*self.net.res_line.p_from_mw[0], 0.008, element = self.l1, side = self.b1)