PROJ_BIN="dbbackup"
PROJ="dbbackup-go"
MODULE="dbm-services/mysql/db-tools/mysql-dbbackup"
VERSION = $(error please set VERSION flag)
DIST = $(error please set DIST flag to txsql or community)
GITHASH = ""
OUTPUT_DIR = build
PKG_DIR=${OUTPUT_DIR}/${PROJ}
PROJ_PKG=${PROJ}-${DIST}.tar.gz
PROJ_PKG_DEPS=dbbackup-go-deps-${DIST}
RELEASE_BUILD_FLAG = "-w -s -X ${MODULE}/cmd.version=${VERSION} -X ${MODULE}/cmd.gitHash=${GITHASH} "
DEV_BUILD_FLAG = "-X ${MODULE}/cmd.version="develop" -X ${MODULE}/cmd.gitHash="" "
BASE_DIR = $(shell pwd)

.PHONY: build
build:
	echo "Building ${OUTPUT_DIR}/${PROJ_BIN}"
	mkdir -p ${OUTPUT_DIR}
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags ${RELEASE_BUILD_FLAG} -gcflags="all=-trimpath=${PWD}" -asmflags="all=-trimpath=${PWD}" -o ${OUTPUT_DIR}/${PROJ_BIN}

.PHONY: package
package:
	make clean
	make build
	echo "Packaging ${PROJ_PKG} using dependency ${PROJ_PKG_DEPS}"
	mkdir -p ${PKG_DIR}
	cp ${OUTPUT_DIR}/${PROJ_BIN} ${PKG_DIR}/
	cp mydumper_for_tdbctl.cnf ${PKG_DIR}/
	cp dbbackup_main.sh ${PKG_DIR}/
	rm -rf ${PROJ_PKG_DEPS} && tar -zxf ${PROJ_PKG_DEPS}.tar.gz
	cp -r ${PROJ_PKG_DEPS}/* ${PKG_DIR}/
	chmod +x ${PKG_DIR}/*.sh && chmod +x ${PKG_DIR}/dbbackup
	chmod +x ${PKG_DIR}/bin/* && chmod +x ${PKG_DIR}/bin/*/*
	tar -C ${OUTPUT_DIR} -zcf ${OUTPUT_DIR}/${PROJ_PKG} ${PROJ}
	md5sum ${OUTPUT_DIR}/${PROJ_PKG}

.PHONY: clean
clean:
	rm -rf ${PKG_DIR}/*
	rm -rf ${OUTPUT_DIR}/${PROJ_PKG}
	rm -rf ${PROJ_PKG_DEPS}
