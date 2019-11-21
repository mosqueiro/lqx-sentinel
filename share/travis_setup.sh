#!/bin/bash
set -evx

mkdir ~/.lqxcore

# safety check
if [ ! -f ~/.lqxcore/.lqx.conf ]; then
  cp share/lqx.conf.example ~/.lqxcore/lqx.conf
fi
