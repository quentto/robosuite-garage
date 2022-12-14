# robosuite-garage

[**robosuite**](https://robosuite.ai/) &ensp; [**robosuite-pickable**](https://github.com/quentto/robosuite-pickable) &ensp; [**garage**](https://github.com/rlworkgroup/garage) &ensp; [**[ARISE Initiative]**](https://github.com/ARISE-Initiative)

-------
## Robosuite environments in garage's SAC
- Robosuite environments are now pickable and can be used by garage samplers
- Use [robosuite-pickable](https://github.com/quentto/robosuite-pickable) forked from version 1.3.2
- Environments can then be used in parallel by algorithms like SAC or MT-SAC (e.g. [garage](http://github.com/rlworkgroup/garage))
- Fixes: """TypeError: no default reduce due to non-trivial cinit"""

-------
## Installation notes & requirements

* virtualenv with python 3.7.10
* mujoco version: mujoco210-linux-x86_64 (installation: [mujoco-py](https://github.com/nimrod-gileadi/mujoco-py))
* importlib_resources==5.4.0
* mujoco-py==2.1.2.14
* gym==0.21.0
* robosuite: [robosuite-pickable](https://github.com/quentto/robosuite-pickable) (forked from version 1.3.2):
```sh
pip install git+https://github.com/quentto/robosuite-pickable.git
```
