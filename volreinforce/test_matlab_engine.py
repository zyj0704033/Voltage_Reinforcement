import matlab
import matlab.engine

eng = matlab.engine.start_matlab()  #start matlab in python
eng.addpath("/home/t630/Voltage_Control/test2")  #add voltage control path to the matlab workspace
eng.start_matpower()  #start up matpower
eng.load_data(nargout=0)
eng.control_sample(nargout=0)
eng.quit()
print("finish test matlab!")
