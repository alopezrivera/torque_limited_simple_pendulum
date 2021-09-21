# Soft Actor Critic Control #

Type: Closed loop, learning based, model free

State/action space constraints: None

Optimal: Yes

Versatility: Swing-up and stabilization

## Theory # 

A controller class to use a model trained by the [sac trainer](software/python/simple_pendulum/reinforcement_learning/sac/README.md).

## Requirements # 
- Stable Baselines 3 (https://github.com/DLR-RM/stable-baselines3)
- Numpy
- PyYaml

## API # 

The class for the SAC Controller initialized by creating an instance as:

    controller = SacController(model_path=model_path,
                               torque_limit=2.0,
                               use_symmetry=True)
with the input:

- model_path: str or path
- torque_limit: torque_limit of the pendulum, the output of the model is scaled with this value
- use_symmetry: whether to use the left/right symmetry of the pendulum

The control output $`\mathbf{u}(\mathbf{x})`$ when given observed state $`\mathbf{x}`$ 
is generated by:

    controller.get_control_output(meas_pos, mean_vel, meas_tau, meas_time)

## Usage #
 An example of how to use this controller can be found in the [sim_sac.py script](software/python/examples/sim_sac.py) in the examples folder.

A fully trained model is saved [here](data/models/sac_model.zip).

## Comments #





