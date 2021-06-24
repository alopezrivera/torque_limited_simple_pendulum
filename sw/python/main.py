# global imports
import sys
import os
import numpy as np
# import asyncio
from datetime import datetime
from pathlib import Path

# local imports
from model import parameters
from controllers import motor_control_loop
from controllers.open_loop.open_loop import *
from controllers.sac.sac_controller import *
from controllers.energy_shaping.energy_shaping_controller import *
# from controllers.ilqr.iLQR_MPC_controller import *
from utilities import parser, process_data, looptime, plot

# set your workspace
WORK_DIR = Path(Path(os.path.abspath(__file__)).parents[2])
print("Workspace is set to:", WORK_DIR)
sys.path.append(f'{WORK_DIR}/sw/python')     # add parent folder to system path

# get a timestamp
TIMESTAMP = datetime.now().strftime("%Y%m%d-%I%M%S-%p")

# run syntax parser
args, unknown = parser.syntax_parser()

# select control method
if args.pd:
    name = "Proportional-Derivative Control"
    folder_name = "pd_control"
    attribute = "open_loop"

    control_method = OpenLoopController()

    # get parameters
    params = control_method.get_params(params_path)

    # prepare data
    (des_time_list, des_pos_list, des_vel_list, des_tau_list, meas_pos_list,
     meas_vel_list, meas_tau_list, meas_time_list, dt, n) = \
        control_method.prepare_data()

    # start control loop for ak80_6
    (start, end, meas_dt, meas_pos, meas_vel, meas_tau, meas_time, des_pos,
     des_vel, des_tau, des_time) = motor_control_loop.ak80_6(control_method,
                                                             name, attribute,
                                                             params, n, dt)
    # if args.qdd100:
    #    (start, end, meas_dt, meas_pos, meas_vel, meas_tau, meas_time) = \
    #        asyncio.run(motor_control_loop.qdd100(CSV_FILE, n, dt,
    #                                              des_pos_out, des_vel_out,
    #                                              des_tau_in, meas_pos,
    #                                              meas_vel, meas_tau,
    #                                              meas_time, gr,
    #                                              rad2outputrev))

    # performance profiler
    looptime.profiler(n, dt, des_time, meas_time, start, end, meas_dt)

    output_folder = str(WORK_DIR) + f'/results/{TIMESTAMP}_' + name

    # plot data
    plot.swingup(output_folder, des_pos, des_vel, des_tau, des_time,
                 meas_pos, meas_vel, meas_tau, meas_time)

    # save measurements
    if args.save:
        process_data.save(output_folder, des_pos, des_vel, des_tau, des_time,
                          meas_pos, meas_vel, meas_tau, meas_time)

if args.tau:
    name = "Feedforward Torque"
    folder_name = "torque_control"
    attribute = "open_loop"
    urdf_file = None
    csv_file = "swingup_300Hz.csv"
    params_file = None
    kp = 0
    kd = 0

    # read data
    (urdf_path, params_path, csv_path, data, n) = process_data.read(
        params_file, urdf_file, csv_file)

    control_method = OpenLoopController()

    # prepare data
    (des_time_list, des_pos_list, des_vel_list, des_tau_list, meas_pos_list,
     meas_vel_list, meas_tau_list, meas_time_list, dt) = \
        control_method.prepare_data(csv_path, n)

    # start control loop for ak80_6
    (start, end, meas_dt, meas_pos, meas_vel, meas_tau, meas_time, des_pos,
     des_vel, des_tau, des_time) = motor_control_loop.ak80_6(control_method,
                                                             name, attribute,
                                                             kp, kd, n, dt)

    # performance profiler
    looptime.profiler(n, dt, des_time, meas_time, start, end, meas_dt)

    output_folder = str(WORK_DIR) + f'/results/{TIMESTAMP}_' + folder_name

    # plot data
    plot.swingup(output_folder, des_pos, des_vel, des_tau, des_time,
                 meas_pos, meas_vel, meas_tau, meas_time)

    # save measurements
    if args.save:
        process_data.save(output_folder, des_pos, des_vel, des_tau, des_time,
                          meas_pos, meas_vel, meas_tau, meas_time)

if args.sac:
    control_method = SacController()    # cm = control_method.return_all()
    name = "Soft Actor Critic"
    folder_name = "sac"
    attribute = "closed_loop"

    # get parameters
    params = control_method.get_params(params_path)

    # prepare data
    prep = control_method.prepare_data(params)

    # start control loop for ak80_6
    (start, end, meas_dt, meas_pos, meas_vel, meas_tau, meas_time, des_pos,
     des_vel, des_tau, des_time) = motor_control_loop.ak80_6(control_method,
                                                             name, attribute,
                                                             params, prep)
    # if args.qdd100:
    #    (start, end, meas_dt, meas_pos, meas_vel, meas_tau, meas_time) = \
    #        asyncio.run(motor_control_loop.qdd100(CSV_FILE, n, dt,
    #                                              des_pos_out, des_vel_out,
    #                                              des_tau_in, meas_pos,
    #                                              meas_vel, meas_tau,
    #                                              meas_time, gr,
    #                                              rad2outputrev))

    # performance profiler
    looptime.profiler(n, dt, des_time, meas_time, start, end, meas_dt)

    output_folder = str(WORK_DIR) + f'/results/{TIMESTAMP}_' + name

    # plot data
    plot.swingup(output_folder, des_pos, des_vel, des_tau, des_time,
                 meas_pos, meas_vel, meas_tau, meas_time)

    # save measurements
    if args.save:
        process_data.save(output_folder, des_pos, des_vel, des_tau, des_time,
                          meas_pos, meas_vel, meas_tau, meas_time)


"""
if args.energy:
    name = "Energy Shaping"
    folder_name = "energy_shaping"
    # urdf_file = "simple_pendulum.urdf"
    # urdf_path = str(WORK_DIR) + "/data/urdf/" + urdf_file
    params_file = "sp_parameters_02.yaml"
    params_path = str(WORK_DIR) + "/data/parameters/" + params_file
    parameters = params.get_params(params_path)
    dt = 0.01
    kp = 0
    kd = 0
    control_method = EnergyShapingController(# parameters,
                                             mass,
                                             length,
                                             damping,
                                             gravity,
                                             0.3)
    control_method.set_goal([np.pi, 0])

    # start control loop
    (start, end, meas_dt, meas_pos, meas_vel, meas_tau, meas_time, des_pos,
     des_vel, des_tau, des_time) = motor_control_loop.ak80_6(control_method,
                                                             kp, kd, n, dt)

    looptime.profiler(n, dt, des_time, meas_time, start, end, meas_dt)

    output_folder = str(WORK_DIR) + f'/results/{TIMESTAMP}_' + name
    plot.swingup(output_folder, des_pos, des_vel, des_tau, des_time,
                 meas_pos, meas_vel, meas_tau, meas_time)

    if args.save:
        process_data.save(output_folder, des_pos, des_vel, des_tau, des_time,
                          meas_pos, meas_vel, meas_tau, meas_time)

if args.lqr:
    looptime.profiler(n, dt, des_time, meas_time, start, end, meas_dt)
    output_folder = str(WORK_DIR) + f'/results/{TIMESTAMP}_' + name

    if args.save:
        process_data.save(output_folder, des_pos, des_vel, des_tau, des_time,
                          meas_pos, meas_vel, meas_tau, meas_time)


if args.ilqr:
    name = "ilqr"
    params_file = "sp_parameters_01.yaml"
    n = 1000
    n_x = 3
    dt = 0.02
    t_final = 10.0
    x0 = np.array([0.0, 0.0])
    x0_sim = x0.copy()
    goal = np.array([np.pi, 0])
    if n_x == 3:
        x0 = np.array([np.cos(x0[0]), np.sin(x0[0]), x0[1]])
        goal = np.array([np.cos(goal[0]), np.sin(goal[0]), goal[1]])

    control_method = iLQRMPCController(# parameter,
                                   mass=mass,
                                   length=length,
                                   damping=damping,
                                   coulomb_friction=coulomb_fric,
                                   gravity=gravity,
                                   x0=x0,
                                   dt=dt,
                                   n=50,  # horizon size
                                   max_iter=1,
                                   break_cost_redu=1e-1,
                                   sCu=1.5,
                                   sCp=50.0,
                                   sCv=1.0,
                                   sCen=0.0,
                                   fCp=20.0,
                                   fCv=1.0,
                                   fCen=0.0,
                                   dynamics="runge_kutta",
                                   n_x=n_x)

    (start, end, meas_dt, meas_pos, meas_vel, meas_tau, meas_time, des_pos,
     des_vel, des_tau, des_time) = motor_control_loop2.ak80_6(control_method, kp,
                                                              kd, n, dt)

    looptime.profiler(n, dt, des_time, meas_time, start, end, meas_dt)
    output_folder = str(WORK_DIR) + f'/results/{TIMESTAMP}_' + name

    if args.save:
        process_data.save(output_folder, des_pos, des_vel, des_tau, des_time,
                          meas_pos, meas_vel, meas_tau, meas_time)

if args.ddp:
    name = "ddp"
    params_file = "sp_parameters_01.yaml"

    looptime.profiler(n, dt, des_time, meas_time, start, end, meas_dt)
    output_folder = str(WORK_DIR) + f'/results/{TIMESTAMP}_' + name

    if args.save:
        process_data.save(output_folder, des_pos, des_vel, des_tau, des_time,
                          meas_pos, meas_vel, meas_tau, meas_time)
"""

if not args:
    print("Control method as input argument required (eg. -pd, -tau, "
          "-lqr; ...).")





