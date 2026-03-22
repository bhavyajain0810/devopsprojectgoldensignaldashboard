# Golden Signal Dashboard — minimal Puppet class for category alignment.
# Renders the same layout as puppet/templates/dashboard.conf.epp via inline_epp
# so it validates without a full modules/ tree; copy the .epp into a module for production.

class golden_signal_dashboard (
  String $app_host = '127.0.0.1',
  Integer $app_port = 8501,
  String $config_path = '/etc/golden-signal-dashboard/dashboard.conf',
) {
  file { '/etc/golden-signal-dashboard':
    ensure => directory,
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }

  $body = inline_epp(
    '<%- | String $app_host, Integer $app_port | -%>
# Managed by Puppet — Golden Signal Dashboard upstream hints
GOLDEN_SIGNAL_APP_HOST=<%= $app_host %>
GOLDEN_SIGNAL_APP_PORT=<%= $app_port %>
',
    { 'app_host' => $app_host, 'app_port' => $app_port }
  )

  file { $config_path:
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => $body,
    require => File['/etc/golden-signal-dashboard'],
  }
}
