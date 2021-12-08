from sbs_vars import SBS_vars

vars = SBS_vars()

distro_name = vars.utils.distro
distro_ver = vars.utils.distro_version
vars.utils.LOG_DEBUG(f"You are running {distro_name} v{distro_ver}.")
if distro_name.upper() in ["ubuntu".upper(), "debian".upper(), "kali".lower(), "raspbian".lower()]:  
    vars.utils.create_file_from_path(
        vars.utils.create_file_from_path(vars.out_dir)
    )
else:
    vars.utils.LOG_ERROR("You are running on an unsupported Linux Distro. Please install either Debian or Ubuntu and try again.")