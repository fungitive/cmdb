from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Asset(models.Model):
    """
    所有资产共有数据表
    """
    asset_type_choice = (
        ('server','服务器'),
        ('storagedevice','存储设备'),
        ('networkdevice','网络设备'),
        ('securitydevice','安全设备'),
        ('software','软件资产'),
    ) #设备类型

    asset_status = (
        (0,'在线'),
        (1,'下线'),
        (2,'未知'),
        (3,'故障'),
        (4,'备用'),
    )#设备状态

    asset_type = models.CharField(choices=asset_type_choice,max_length=64,default='server',verbose_name='资产类型')
    name = models.CharField(max_length=64,unique=True,verbose_name='资产名称')#不可重复
    sn = models.CharField(max_length=128,unique=True,verbose_name='资产编号')#不可重复
    business_unit = models.ForeignKey('BusinessUnit',null=True,blank=True,verbose_name='所属业务线',
                                      on_delete=models.SET_NULL)
    status = models.SmallIntegerField(choices=asset_status,default=0,verbose_name='设备状态')
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name='制造商',
                                     on_delete=models.SET_NULL)
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP',)
    tags = models.ManyToManyField('Tag',blank=True, verbose_name='标签',)
    admin = models.ForeignKey(User,null=True, blank=True, verbose_name='资产管理员',related_name='admin',
                              on_delete=models.SET_NULL)
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='所在机房',on_delete=models.SET_NULL)
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='合同',on_delete=models.SET_NULL)
    purchase_day = models.DateField(null=True, blank=True, verbose_name='购买日期',)
    expire_day = models.DateField(null=True, blank=True, verbose_name='过保日期', )
    price = models.FloatField(null=True, blank=True, verbose_name='价格', )
    approved_by = models.ForeignKey(User,null=True, blank=True, verbose_name='批准人',related_name='approved_by',
                                    on_delete=models.SET_NULL)
    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True,verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now=True,verbose_name='更新日期')

    def __str__(self):
        return '<%s>  %s' % (self.get_asset_type_display(),self.name)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"
        ordering = ['-c_time']

class BusinessUnit(models.Model):
    """ 业务线 """
    name = models.CharField(max_length=64, unique=True, verbose_name='业务线名称')
    parent_unit = models.ForeignKey('self',blank=True,null=True,related_name='parent_level',
                                    on_delete=models.CASCADE)
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"

class Manufacturer(models.Model):

    """ 制造商，厂商 """
    name = models.CharField(max_length=64, unique=True, verbose_name='厂商名称')
    telephone = models.CharField(max_length=30,blank=True,null=True,verbose_name='支持电话')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"

class Tag(models.Model):
    """ 标签 """
    name = models.CharField(max_length=32, unique=True, verbose_name='标签名')
    c_day = models.DateField(verbose_name='创建日期',auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"

class IDC(models.Model):
    """ 机房 """
    name = models.CharField(max_length=64,unique=True,verbose_name='机房名称')
    memo = models.CharField(max_length=128, blank=True,null=True, verbose_name='机房名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"

class Contract(models.Model):
    """ 合同 """
    sn = models.CharField(max_length=128, unique=True,verbose_name='合同编号')
    name = models.CharField(max_length=32, verbose_name='合同名称')
    memo = models.TextField(blank=True,null=True,verbose_name='备注')
    price = models.IntegerField(verbose_name='合同金额')
    detail = models.TextField(null=True,blank=True,verbose_name='合同详细')
    start_day = models.DateField(blank=True,null=True,verbose_name='开始日期')
    end_day = models.DateField(blank=True,null=True,verbose_name='失效日期')
    license_num = models.IntegerField(blank=True,null=True,verbose_name='license数量')
    c_day = models.DateField(verbose_name='创建日期',auto_now_add=True)
    m_day = models.DateField(verbose_name='更新日期', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"

class Server(models.Model):
    """ 服务器设备 """
    sub_asset_type_choice = (
        (0,'塔式'),
        (1,'机架式'),
        (2,'刀片式'),
        (3,'小型机'),
    )#服务器设备类型

    created_by_chioce = (
        ('auto','自动添加'),
        ('manual','手动录入'),
    )

    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice,default=0,verbose_name='服务器类型')
    created_by = models.CharField(choices=created_by_chioce,max_length=32,default='auto',verbose_name='添加方式')
    hosted_on = models.ForeignKey('self',related_name='hosted_on_server',null=True,blank=True,
                                  verbose_name='宿主机',on_delete=models.CASCADE)#虚拟机专用字段
    model = models.CharField(max_length=128,null=True,blank=True,verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, null=True, blank=True, verbose_name='Raid类型')
    os_type = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统类型')
    os_distribution = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统发行商')
    os_release = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统版本')

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name,self.get_sub_asset_type_display(),self.model,self.asset.sn)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"

class SecurityDevice(models.Model):
    """ 安全设备 """
    sub_asset_type_choice = (
        (0,'防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (3, '运维审计系统'),
    )
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='安全设备类型')
    model = models.CharField(max_length=128,default='未知型号',verbose_name='安全设备型号')

    def __str__(self):
        return self.asset.name + "--"+self.get_sub_asset_type_display()+ str(self.model) + 'id:%s'% self.id

    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = "安全设备"

class StorageDevice(models.Model):
    """ 存储设备 """
    sub_asset_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'),
        (2, '磁盘库'),
        (3, '磁带机'),
    )
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='存储设备类型')
    model = models.CharField(max_length=128,default='未知型号',verbose_name='存储设备型号')

    def __str__(self):
        return self.asset.name + "--"+self.get_sub_asset_type_display()+ str(self.model) + 'id:%s'% self.id

    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = "存储设备"

class NetworkDevice(models.Model):
    """ 网络设备 """
    sub_asset_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (3, '运维审计系统'),
    )
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='网络设备类型')
    model = models.CharField(max_length=128,default='未知型号',verbose_name='网络设备型号')
    vlan_ip = models.GenericIPAddressField(blank=True,null=True,verbose_name='VLanIP')
    intrantet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='内网IP')
    firmware = models.CharField(max_length=128,blank=True, null=True, verbose_name='设备固件版本')
    port_num = models.SmallIntegerField(null=True,blank=True,verbose_name='端口个数')
    device_detail = models.TextField(null=True,blank=True,verbose_name='详细配置')

    def __str__(self):
        return '%s--%s--%s ,sn:%s>' % (self.asset.name,self.get_sub_asset_type_display(),self.model,self.asset.sn)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"

class Software(models.Model):
    """ 只保存付费购买的软件 """
    sub_asset_type_choice = (
        (0, '操作系统'),
        (1, '办公/开发软件'),
        (2, '业务软件'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='软件类型')
    license_num = models.IntegerField(default=1,verbose_name='授权数量')
    version = models.CharField(max_length=64,unique=True,help_text='例如: RedHat release 7 (Final)',
                               verbose_name='软件/系统版本')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(),self.version)

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = "软件/系统"

class CPU(models.Model):
    """ CPU组件"""

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    cpu_model = models.CharField(max_length=128,blank=True,null=True,verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField(default=1,verbose_name='物理CPU个数')
    cpu_core_count = models.PositiveSmallIntegerField(default=1, verbose_name='CPU核数')

    def __str__(self):
        return self.asset.name + ": " +self.cpu_model

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = "CPU"

class RAM(models.Model):
    """ 内存组件"""

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField(max_length=128,blank=True,null=True,verbose_name='SN号')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='内存型号')
    manufactory = models.CharField(max_length=128, blank=True, null=True, verbose_name='内存制造商')
    slot = models.CharField(max_length=128, verbose_name='插槽位')
    capacity = models.IntegerField(null=True,blank=True,verbose_name='内存大小(GB)')

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.name,self.model,self.slot,self.capacity)

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = "内存"
        unique_together = ('asset', 'slot')#同一资产下的内存，根据卡槽的不同必须唯一

class Disk(models.Model):
    """ 硬盘组件"""
    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField(max_length=128,blank=True,null=True,verbose_name='硬盘SN号')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='硬盘型号')
    manufactory = models.CharField(max_length=128, blank=True, null=True, verbose_name='硬盘制造商')
    slot = models.CharField(max_length=128, verbose_name='插槽位')
    capacity = models.IntegerField(null=True,blank=True,verbose_name='磁盘容量(GB)')
    interface_type = models.CharField(max_length=16,choices=disk_interface_type_choice, verbose_name='接口类型')

    def __str__(self):
        return '%s: %s: %s: %sGB' % (self.asset.name,self.model,self.slot,self.capacity)

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"
        unique_together = ('asset', 'sn')#同一资产下的硬盘，根据硬盘SN的不同必须唯一

class NIC(models.Model):
    """ 网卡组件"""

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    name = models.CharField(max_length=64,blank=True,null=True,verbose_name='网卡名称')
    model = models.CharField(max_length=128, verbose_name='网卡型号')
    mac = models.CharField(max_length=64,  verbose_name='MAC地址')
    ip_address = models.GenericIPAddressField(blank=True,null=True,verbose_name='IP地址')
    netmask = models.GenericIPAddressField(blank=True, null=True, verbose_name='掩码')
    bonding = models.GenericIPAddressField(blank=True, null=True, verbose_name='绑定地址')


    def __str__(self):
        return '%s: %s: %s' % (self.asset.name,self.model,self.mac)

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = "网卡"
        unique_together = ('asset', 'model','mac')#资产、型号和mac必须联合唯一

class EventLog(models.Model):
    """ 日志 """
    event_type_choice = (
        (0, '其他'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线/变更/更新'),
    )
    name = models.CharField(max_length=128,verbose_name='事件名称')
    asset = models.ForeignKey('Asset', null=True,blank=True,on_delete=models.CASCADE)
    new_asset = models.ForeignKey('NewAssetApprovalZone',null=True,blank=True,on_delete=models.SET_NULL)
    event_type = models.SmallIntegerField(default=4,choices=event_type_choice,verbose_name='设备类型')
    component = models.TextField(max_length=256,null=True,blank=True,verbose_name='事件子项')
    detail = models.TextField(verbose_name='事件详情')
    date = models.DateTimeField(auto_now_add=True,verbose_name='事件时间')
    user = models.ForeignKey(User,null=True,blank=True,verbose_name='事件执行人',on_delete=models.CASCADE)
    memo = models.TextField(null=True,blank=True,verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件记录'
        verbose_name_plural = "事件记录"

class NewAssetApprovalZone(models.Model):
    """ 新资产待审批区 """
    sn = models.CharField('资产SN号', max_length=128, unique=True)  # 此字段必填
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
    )
    asset_type = models.CharField(choices=asset_type_choice, default='server', max_length=64, blank=True, null=True,
                                  verbose_name='资产类型')
    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='生产厂商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField(verbose_name='CPU物理数量', blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField(verbose_name='CPU核心数量', blank=True, null=True)
    os_distribution = models.CharField(verbose_name='发行商', max_length=64, blank=True, null=True)
    os_type = models.CharField(verbose_name='系统类型', max_length=64, blank=True, null=True)
    os_release = models.CharField(verbose_name='操作系统版本号', max_length=64, blank=True, null=True)
    data = models.TextField(verbose_name='资产数据')  # 此字段必填
    c_time = models.DateTimeField(verbose_name='汇报日期', auto_now_add=True)
    m_time = models.DateTimeField(verbose_name='数据更新日期', auto_now=True)
    approved = models.BooleanField(verbose_name='是否批准', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"
        ordering = ['-c_time']













