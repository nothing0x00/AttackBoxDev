## AttackBox v1

### Summary
The AttackBox grew out of a series of problems which were presented by the COVID-19 pandemic, specifically, the inability to travel to client sites to perform internal network pentests and wireless penetration testing. To remedy this issue we tried other remote pentesting frameworks (and have sourced ideas, heavily, from them), but, decided that the modifications necessary to get them to fit our needs were not the most efficient use of our time. As a result, we built the AttackBox, from the ground up, as a cross-platform remote penetration testing framework, which has the following features:


- The AttackBox uses reverse SSH for connections to a server, eliminating the need for clients to forward ports.
- Uses commonly utilized tools, many of which are available either as part of the Linux kernel, or as part of Kali Linux, by default, in order to provide a toolset most pentesters would be comfortable with. This can, of course, be customized.
- The framework is modular, and allows for different configurations of machine to be constructed with simple commandline flags.
- The completed device will be able to operate with a fully encrypted hard drive, eliminating the risk of data being intercepted in transit to or from the client.
- The completed device will contain the tooling necessary for internal penetration tests, as well as remote wireless penetration testing.
- The AttackBox scripts can be used to install necessary tooling, and configure connections, on a wide array of devices and platforms, including the NUC, the Raspberry Pi and on virtual machines, each with installation scripts specifically configured for these devices.
- The reverse SSH connection is auto-healing for resiliency.
- Framework provides a fallback form of command and control in the event that the reverse SSH connection fails. This is still in development, but will use a simple process in which the client polls a publicly available file hosted online for commands.
- Due to the ability to be cross platform, the AttackBox can be used on physical penetration tests as a dropbox.
- Connections to the AttackBox can occur through a minimal VPS instance configured to operate as a jump box.
- Clients can install the AttackBox with minimal instructions.


### Structure of the Repsitory

The repsitory contains a variety of tools, configuration files and scripts which make the AttackBox installation and operation process function smoothly. Within this repsitory one will find the following content:

- configs: This directory contains configuration files for a variety of services which will be configured during the installation process.
- modules: This directory contains the Python modules used in the installation script. We kept the framework modular to facilitate customization and debugging.
- scripts: This directory includes various scripts which can either be used during testing, such as the wificonnect.py script, or which are utilized during normal operations of the framework.

### Hardware

The AttackBox can be installed on a wide array of hardware platforms, but we have found the most success with the Intel NUC and the Raspberry Pi 4.

#### Intel NUC

- Processor: i5 or better
- RAM: 8 GB or better
- SSD: 60GB or better


#### Raspberry Pi 4
- RAM: 4 GB
- SD Card: 60GB or better

### Installation and Configuration Process

#### Kali Installation

The AttackBox itself is built off of Kali Linux, and the process starts with installing Kali Linux on the device that will be used on the client site. The installation of Kali is outside of the scope of this README, but there are a couple of notes here:

- When installing Kali make sure to encrypt the drive with a password. In future iterations there will be a process put in place to decrypt the drive on boot using a USB key, with the password as a fallback, but for now the password will be sent to the client for decrypting the drive on boot.

- If you would like the ability to do X-Forwarding, make sure to install a desktop environment.

**Installation Instruction Links**

Installing Kali on a NUC or in a Virtual Machine(or any other full featured computer for that matter):

https://www.kali.org/docs/installation/

Link to Pre-Built Kali Virtual Machine Images:

https://www.offensive-security.com/kali-linux-vm-vmware-virtualbox-image-download/

Installing Kali on the Raspberry Pi 4

https://www.kali.org/news/raspberry-pi-4-and-kali/

#### USB Key Creation

Jon, fill this in when possible

#### Public Server

The public server component is used by the client machine to connect back to, and is used as a jump box for command and control.

Due to some of the configurations utilized for securing the SSH connections out of the client network, the public machine needs to be running an updated Debian derived operating system, with the best results being seen while using Ubuntu Server 20.04.

This can be set up on any provider that can provide a public IP. In our configurations, we tend to attach this IP to a subdomain to make routing easier, and allow us to shift IPs if necessary.

#### Installation Process

All variants of the installation start with pulling down the repository.

`git clone https://github.com/nothing0x00/AttackBoxDev.git`

And then entering the directory:

`cd AttackBoxDev`

**Public Server**

Before running this module, make sure to set up DNS for this IP; there is an automated Let's Encrypt certificate generation process as a part of this module.

Once the repository is pulled down, to install the public server framework, run the following command:

`sudo attackbox.py public`

This module is interactive, and will pause execution before completing, while awaiting for the SSH configuration process is completed on the client side.  The client side module will generate and upload SSH keys to this public server, to allow for the reverse SSH connection to be able to be completed, and for the connection to be set to automatically heal.

**Client Installation**

The client machine installation process has a variety of possible options, each based on modules in the modules/ directory.

The help menu shows the following main options:

```positional arguments:
  {public,client,custom}
    public              Installs and Configures Public C2 Server
    client              Installs and Configures Specific Client System
    custom              Installs and configures selected modules
```
We covered the public argument above, in the Public Server installation.

The client argument allows for the user to install a pre-configured client environment, which is based on running a number of specific modules.

The custom arguments allows for the user to install specific modules, which is useful to extend functionality on an already configured client machine.

In the client menu the options are the following:

```
usage: attackbox.py client [-h] [--all | --rpi | --vm | --nuc]

optional arguments:
  -h, --help  show this help message and exit
  --all       Install and configure all client modules
  --rpi       Installs and configures Raspberry Pi Physical Pentest Dropbox
  --vm        Installs and configures Pentest Virtual Machine
  --nuc       Installs and confgures Intel NUC Physical Pentest Dropbox
  ```

  The custom menu provides the following options:

  ```
  usage: attackbox.py custom [-h] [-a] [-i] [-w] [-v] [-c] [-l] [-u]

optional arguments:
  -h, --help      show this help message and exit
  -a, --autossh   Installs and configures autossh
  -i, --internal  Installs tools for a internal pen test
  -w, --wireless  Installs tools for a wireless pen test
  -v, --vnc       Installs and configures VNC
  -c, --c2        Installs and configures HTTP Command Polling
  -l, --client    Installs client-side post-deployment configuration script
  -u, --update    Installs updates
```

#### Scripts

In the scripts directory there are various helper scripts which can aid in elements of testing, specifically wireless testing, which can sometimes lead to issues.

Many of these scripts are used in setting up other elements of the framework, the scripts listed below will be run by a tester during an engagement:

http_c2_command.py: When the HTTP command and control modules are completed, this will allow a tester to have an interface through which they can send commands to the client machine. This is not an interactive shell, it merely allows for inputting commands into a file which will be retrieved by the client machine.

wifi_connect.py: A simple command line wireless interface, allowing for easy connection to a wireless network without accidentally dropping the Linux network stack.

wireless_control.py: A script to make it easy to set an interface into monitor mode, or set it back into managed mode, without dropping the whole Linux network stack, through a combination of nmcli and airmon.

### Functionality

After the client script completes execution, and the public server script has been reactivated, and has completed execution, the next step is to test the connection.

Start the process by rebooting the client machine. Currently, this process will necessitate a screen and a keyboard in order to input the decryption key to unlock the drive and complete the booting process. In the future, this process will be able to be completed by inserting a USB stick into the machine, which will allow for a key to be transferred to the machine, to unlock the drive, without needing to manually input the key.

On reboot, if everything has gone well, it will automatically connect to the public server.

To test the connection, connect to the public server over SSH.

`ssh root@[ip or domain]`

After connection is established connect to the client machine through SSH using the port identified during installation:

`ssh autossh@localhost -p [port]`

If successful, a connection should open between the client machine and the public server, which will allow the user to control the client machine.

### Client Setup Instructions

When the machine gets to the client site the client will need to complete the following steps currently:

* Remove AttackBox, wireless dongles, wireless dongle bases, power supply and USB extension cables from the box

* If one has been engaged for wireless testing:

  * Plug the USB wireless dongles onto the wireless dongle bases

  * Connect the USB extension cables to the cable coming from the wireless dongle bases

  * Connect USB extension cables to the AttackBox

* Connect ethernet cable to the AttackBox

* Connect screen to AttackBox with an HDMI cable

* Connect keyboard to the AttackBox

* Connect the power supply to the AttackBox

* Turn AttackBox on and allow it to boot

* When asked, input the password for your AttackBox into the prompt to decrypt the hard drive
    Password: [put password here]

* Disconnect screen and keyboard, if you would like. The AttackBox will complete the booting process and initiate a reverse SSH connection out to a server configured for this engagement. Testing will occur through this server.

* Leave AttackBox running for the duration of the engagement

Following implementation of the USB unlocking process the instructions will be simplified to the following:

* Remove AttackBox, wireless dongles, wireless dongle bases, power supply, USB stick and USB extension cables from the box

* If one has been engaged for wireless testing:

  * Plug the USB wireless dongles onto the wireless dongle bases

  * Connect the USB extension cables to the cable coming from the wireless dongle bases

  * Connect USB extension cables to the AttackBox

* Connect ethernet cable to the AttackBox

* Connect USB stick to the AttackBox

* Connect the power supply to the AttackBox

* Turn AttackBox on and allow it to boot. The AttackBox will complete the booting process and initiate a reverse SSH connection out to a server configured for this engagement. Testing will occur through this server.

* Leave AttackBox running for the duration of the engagement
