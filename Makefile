# Makefile for source rpm: NetworkManager
# $Id$
NAME := NetworkManager
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
