{ pkgs, lib, config, inputs, ... }:

{
  dotenv.enable = true;

  packages = [
  	pkgs.git
	pkgs.openldap
	pkgs.gcc
  	pkgs.openssl
	pkgs.cyrus_sasl
	pkgs.postgresql
	pkgs.tree-sitter
	];

  languages.python = {
	enable = true;
	version = "3.11";
	manylinux.enable = false;
	uv.enable = true;
  };
      services.postgres = {
	enable = true;
	listen_addresses = "127.0.0.1";
	port = 5436;
	initialDatabases = [
	{
		name = "apis-oeai";
	}
	];
	initialScript = ''
      CREATE EXTENSION IF NOT EXISTS pg_trgm;
      CREATE EXTENSION IF NOT EXISTS unaccent;
    '';
  };
  enterShell = ''
source .devenv/state/venv/bin/activate
'';

}
