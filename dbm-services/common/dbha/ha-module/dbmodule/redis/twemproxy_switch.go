package redis

import (
	"fmt"

	"dbm-services/common/dbha/ha-module/constvar"
	"dbm-services/common/dbha/ha-module/log"
)

// TwemproxySwitch twemproxy switch instance
type TwemproxySwitch struct {
	RedisProxySwitchInfo
}

// CheckSwitch nothing to check
func (ins *TwemproxySwitch) CheckSwitch() (bool, error) {
	return true, nil
}

// DoSwitch kick twemproxy from gateway
func (ins *TwemproxySwitch) DoSwitch() error {
	ins.ReportLogs(constvar.InfoResult,
		fmt.Sprintf("handle twemproxy switch[%s:%d]", ins.Ip, ins.Port))
	err := ins.KickOffDns()
	cErr := ins.KickOffClb()
	pErr := ins.KickOffPolaris()
	if err != nil {
		tpErrLog := fmt.Sprintf("Twemproxy kick dns failed,err:%s", err.Error())
		log.Logger.Errorf("%s info:%s", tpErrLog, ins.ShowSwitchInstanceInfo())
		ins.ReportLogs(constvar.FailResult, tpErrLog)
		return err
	}
	if cErr != nil {
		tpErrLog := fmt.Sprintf("Twemproxy kick clb failed,err:%s", cErr.Error())
		log.Logger.Errorf("%s info:%s", tpErrLog, ins.ShowSwitchInstanceInfo())
		ins.ReportLogs(constvar.FailResult, tpErrLog)
		return cErr
	}
	if pErr != nil {
		tpErrLog := fmt.Sprintf("Twemproxy kick polaris failed,err:%s", pErr.Error())
		log.Logger.Errorf("%s info:%s", tpErrLog, ins.ShowSwitchInstanceInfo())
		ins.ReportLogs(constvar.FailResult, tpErrLog)
		return pErr
	}
	succLog := fmt.Sprintf("Twemproxy do switch ok,dns[%t] clb[%t], polaris[%t]",
		ins.ApiGw.DNSFlag, ins.ApiGw.CLBFlag, ins.ApiGw.PolarisFlag)
	ins.ReportLogs(constvar.InfoResult, succLog)
	return nil
}

// RollBack TODO
func (ins *TwemproxySwitch) RollBack() error {
	return nil
}

// UpdateMetaInfo nothing to update
func (ins *TwemproxySwitch) UpdateMetaInfo() error {
	return nil
}

// ShowSwitchInstanceInfo show switch instance information
func (ins *TwemproxySwitch) ShowSwitchInstanceInfo() string {
	format := `<%s#%d IDC:%d Status:%s App:%s ClusterType:%s MachineType:%s Cluster:%s> switch`
	str := fmt.Sprintf(
		format, ins.Ip, ins.Port, ins.IdcID, ins.Status, ins.App,
		ins.ClusterType, ins.MetaType, ins.Cluster,
	)
	return str
}
