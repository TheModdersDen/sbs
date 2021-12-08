from utils import Utils

utils = Utils()

distro_name = utils.distro
distro_ver = utils.distro_version
utils.LOG_DEBUG(f"You are running {distro_name} v{distro_ver}.")
if distro_name in ["Ubuntu".lower(), "Debian".lower(), "Kali".lower(), "raspbian".lower()]:  
    utils.create_file_from_path(
        vars.out_dir
    )
else:
    utils.LOG_ERROR("You are running on an unsupported Linux Distro. Please install either Debian or Ubuntu and try again.")