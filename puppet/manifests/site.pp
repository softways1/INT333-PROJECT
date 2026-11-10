# Puppet Manifest: System Configuration Baseline & Docker Management
# Course: INT333 | Project: AI Powered Resume Analyzer

node default {

  # 1. Base System Hardening & Essential Packages
  $base_packages = [
    'apt-transport-https',
    'ca-certificates',
    'curl',
    'gnupg',
    'git',
    'htop',
    'unzip',
    'ufw',
    'nagios-nrpe-server',
    'monitoring-plugins'
  ]

  package { $base_packages:
    ensure => installed,
  }

  # 2. DevOps Application Directory
  file { '/opt/ai-resume-analyzer':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
  }

  # 3. Host MOTD Banner (Baseline enforcement proof)
  file { '/etc/motd':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => "====================================================\n AI Powered Resume Analyzer - DevOps Server\n Managed by: Puppet Configuration Management\n Student: AMAN KUMAR SINGH | Course: INT333\n====================================================\n",
  }

  # 4. Ensure Docker Service is running and enabled
  service { 'docker':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    hasstatus  => true,
  }

  # 5. User Group Membership - ensure ubuntu is in docker group
  user { 'ubuntu':
    ensure => present,
    groups => ['docker'],
  }

  # 6. Ensure Nagios NRPE Service is configured and running
  service { 'nagios-nrpe-server':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    require    => Package['nagios-nrpe-server'],
  }

  # 7. NRPE Custom Configuration for Resource Monitoring
  file { '/etc/nagios/nrpe.d/custom_checks.cfg':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => "command[check_users]=/usr/lib/nagios/plugins/check_users -w 5 -c 10\ncommand[check_load]=/usr/lib/nagios/plugins/check_load -r -w .15,.10,.05 -c .30,.25,.20\ncommand[check_disk]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -p /\ncommand[check_zombie_procs]=/usr/lib/nagios/plugins/check_procs -w 5 -c 10 -s Z\ncommand[check_total_procs]=/usr/lib/nagios/plugins/check_procs -w 150 -c 200\n",
    notify  => Service['nagios-nrpe-server'],
    require => Package['nagios-nrpe-server'],
  }
}
