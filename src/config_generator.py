class ConfigGenerator:
    def __init__(self):
        self.config_template = """configure terminal 
interface gpon-olt_1/{槽位}/{端口}
  onu {ONU编号} type ZTEG-F660 sn {PONSN}  
!
configure terminal 
interface gpon-onu_1/{槽位}/{端口}:{ONU编号} 
  tcont 1 name Tl1DefaultCreate  profile FTTH_UPBW
  gemport 1 name Tl1DefaultCreate  tcont 1
  gemport 1 traffic-limit downstream FTTH_DOWNBW 
  service-port 1 vport 1 user-vlan {有线1UserVLAN} vlan {有线1内层VLAN} svlan {有线1外层VLAN}
  service-port 2 vport 1 user-vlan {无线2GUserVLAN} vlan {无线2G内层VLAN} svlan {无线2G外层VLAN} 
  service-port 3 vport 1 user-vlan {无线5GUserVLAN} vlan {无线5G内层VLAN} svlan {无线5G外层VLAN} 
  service-port 4 vport 1 user-vlan {管理UserVLAN} vlan {管理内层VLAN} svlan {管理外层VLAN}
!
configure terminal    
pon-onu-mng gpon-onu_1/{槽位}/{端口}:{ONU编号} 
service Tl1DefaultCreate gemport 1
vlan port eth_0/1 mode tag vlan {有线1UserVLAN}
vlan port eth_0/2 mode tag vlan {管理UserVLAN}
vlan port wifi_0/1 mode tag vlan {无线2GUserVLAN}
vlan port wifi_0/2 mode tag vlan {无线5GUserVLAN}
!
"""

    def generate_config(self, row_data):
        """根据每行数据生成配置"""
        try:
            return self.config_template.format(**row_data)
        except KeyError as e:
            raise Exception(f"数据缺少必要字段: {str(e)}")

    def save_config(self, config, output_path):
        """保存生成的配置到文件"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(config)
        except Exception as e:
            raise Exception(f"保存配置文件失败: {str(e)}") 