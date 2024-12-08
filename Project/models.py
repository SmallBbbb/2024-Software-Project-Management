

from django.core.exceptions import ValidationError
from django.db import models
# class MyModel(models.Model):
#
#     def __str__(self):
#         return self
'''
用户模型(User)
    ID           INT       即用户ID,为用户的唯一标识符(此项为主键)
    Username     TEXT(20)  用户名,即登陆账号,
    Password     TEXT(20)  登陆密码
    Name         TEXT(20)  用户的真实姓名
    PhoneNumber  TEXT(20)  用户的电话号码
    Institution  TEXT(20)  用户所属机构       
    Identity     TEXT(20)  用户身份,支持人员|测试人员|管理员|潜在客户
    注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''
class User(models.Model):
    #数据表列
    Username = models.CharField(max_length=20, null=False, unique=True)
    Password = models.CharField(max_length=20, unique=False, null=False)
    Name = models.CharField(max_length=20, null=False, unique=True)
    PhoneNumber = models.CharField(max_length=20)
    Institution = models.CharField(max_length=20, null=False)
    Identity = models.CharField(max_length=20, null=False)

    #约束
    class Meta:
        #约束 Identity 的值为 SupportStaff | TestStaff | Administer | PotentialCustomer
        constraints = [
            models.CheckConstraint(
                check=models.Q(Identity='SupportStaff') |
                      models.Q(Identity='TestStaff') |
                      models.Q(Identity='Administer') |
                      models.Q(Identity='PotentialCustomer'),
                name='CheckUserIdentity'
            ),
        ]
    def __str__(self):
        return self

'''
授权证书模型(Certification)
    ID                  INT         证书ID
    Number              INT         证书编号
    Staff               TEXT(20)    被授予证书的测试人员的真实姓名
    Date                DATETIME    授予证书时间
    Category	        TEXT(50)	标准所在的具体类别
    StandardName	    TEXT(50)	标准名称
    StandardNumber      TEXT(50)    标准号(含年号)
    ClauseNumber        TEXT(10)    条款号
    Project             TEXT(50)    项目名称
    Authority           TEXT(50)    签发单位
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''
class Certification(models.Model):

    Number = models.IntegerField(unique=True, null=False)
    StaffUsername = models.CharField(max_length=20, null=False)
    Staff = models.CharField(max_length=20, null=False)
    Date = models.DateTimeField()
    Category = models.CharField(max_length=50, null=False)
    StandardName = models.CharField(max_length=50, null=False)
    StandardNumber = models.CharField(max_length=50, null=False)
    ClauseNumber = models.CharField(max_length=50, null=False)
    Project = models.CharField(max_length=50, null=False)
    Authority = models.CharField(max_length=50, null=False)

    def clean(self):
        # 验证以下二元组是否确实对应 User 模型中的一行
        try:
            User.objects.get(
                Name=self.Staff
            )
        except User.DoesNotExist:
            raise ValidationError({'Name': 'User does not exist.'})
        # 验证以下五元组是否确实对应 Standard 模型中的一行
        try:
            Standard.objects.get(
                Category=self.Category,
                StandardName=self.StandardName,
                StandardNumber=self.StandardNumber,
                ClauseNumber=self.ClauseNumber,
                Project=self.Project,
            )
        except Standard.DoesNotExist:
            raise ValidationError({'Standard': 'Standard does not exist.'})


    def __str__(self):
        return self

'''
标准模型(Standard)
    ID	            INT	        标准在此表中的ID
    BroadCategory	TEXT(50)	标准所在的大类
    Category	    TEXT(50)	标准所在的具体类别
    Project	        TEXT(50)	标准所规定的项目的名称
    StandardName	TEXT(50)	标准名称
    StandardNumber	TEXT(50)	标准号
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''
class Standard(models.Model):

    BroadCategory = models.CharField(max_length=50, null=False)
    Category = models.CharField(max_length=50, null=False)
    Project = models.CharField(max_length=50, null=False)
    StandardName = models.CharField(max_length=50, null=False)
    StandardNumber = models.CharField(max_length=50, null=False)

    #约束
    class Meta:
        #确保以下五元组的唯一性
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'Category',
                    'Project',
                    'StandardName',
                    'StandardNumber'
                    ),
                name='UniqueStandard'
            )
        ]

    def __str__(self):
        return f"{self.StandardName} ({self.StandardNumber})"

'''
项目模型(Project)
    ID	            INT	        项目在此表中的ID
    BroadCategory	TEXT(50)	标准所在的大类
    Category	    TEXT(50)	标准所在的具体类别
    Project 	    TEXT(50)	项目的名称
    StandardName	TEXT(50)	项目所对应标准的名称
    StandardNumber	TEXT(50)	项目所对应标准的标准号
    ClauseNumber	TEXT(50)	项目所对应标准中具体的的条款号
    Staff	        TEXT(50)	开展项目所需的人员
    Equipment	    TEXT(200)	开展项目所需的设备
    Procedure   	TEXT(50)	该项目所需的操作规程
    Sample	        TEXT(200)	该项目的所需的待检测样品
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''

class Project(models.Model):
    BroadCategory = models.CharField(max_length=50, null=False)
    Category = models.CharField(max_length=50, null=False)
    Project = models.CharField(max_length=50, null=False)
    StandardName = models.CharField(max_length=50, null=False)
    StandardNumber = models.CharField(max_length=50, null=False)
    ClauseNumber = models.CharField(max_length=50, null=False)
    Staff = models.CharField(max_length=50, null=False)
    Equipment = models.CharField(max_length=200, null=False)
    Procedure = models.CharField(max_length=50, null=False)
    Sample = models.CharField(max_length=200, null=False)

    # 设置 default 为一个已存在的标准实例
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='projects')  # 假设 ID 为 1 的 Standard 是默认的

    def clean(self):
        try:
            Standard.objects.get(
                Category=self.Category,
                Project=self.Project,
                StandardName=self.StandardName,
                StandardNumber=self.StandardNumber,
            )
        except Standard.DoesNotExist:
            raise ValidationError({'Standard': 'Standard does not exist.'})

    def __str__(self):
        return f"{self.Project} - {self.StandardName} ({self.StandardNumber})"

'''
测试人员模型(TestStaff)
    ID	                INT	        测试人员在本表中的ID
    Name	            TEXT(20)	测试人员的真实姓名
    Category	        TEXT(50)	测试人员有资格参与的项目所属的类别
    Project 	        TEXT(50)	测试人员有资格参与的项目的名称
    StandardName	    TEXT(50)	测试人员有资格参与的项目所属标准的名称
    StandardNumber  	TEXT(50)	测试人员有资格参与的项目所属标准的标准号
    ClauseNumber	    TEXT(50)	测试人员有资格参与的项目所属条款的条款号
    TraFinTime	        DATETIME	测试人员完成培训的时间
    TraCertification	TEXT(100)	测试人员所获培训证书的链接
    ExamTime	        DATETIME	测试人员完成考核的时间
    TestFile	        TEXT(100)	测试人员考核文件的链接
    AuthCertification	TEXT(100)	测试人员所获授权证书的链接
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''

class TestStaff(models.Model):

    Name = models.CharField(max_length=20, null=False, unique=True)
    Category = models.CharField(max_length=50, null=False)
    Project = models.CharField(max_length=50, null=False)
    StandardName = models.CharField(max_length=50, null=False)
    StandardNumber = models.CharField(max_length=50, null=False)
    ClauseNumber = models.CharField(max_length=50, null=False)
    TraFinTime = models.DateTimeField()
    TraCertification = models.CharField(max_length=100, null=False, unique=True)
    ExamTime = models.DateTimeField()
    TestFile = models.CharField(max_length=100, null=False, unique=True)
    AuthCertification = models.CharField(max_length=100, null=False, unique=True)

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='projects1')


    def clean(self):
        # 验证 Name 是否确实对应 User 模型中的 Name
        try:
            User.objects.get(
                Name=self.Name,
            )
        except User.DoesNotExist:
            raise ValidationError({'Name': 'User does not exist.'})
        # 验证以下五元组是否确实对应 Standard 模型中的一行
        try:
            Project.objects.get(
                Category=self.Category,
                Project=self.Project,
                StandardName=self.StandardName,
                StandardNumber=self.StandardNumber,
                ClauseNumber=self.ClauseNumber
            )
        except Project.DoesNotExist:
            raise ValidationError({'Project': 'Project does not exist.'})

    def __str__(self):
        return f"{self.Project} - {self.StandardName} ({self.StandardNumber})"

'''
设备模型(Equipment)
    ID	            INT	设备在本表中的ID
    Category	    TEXT(50)	使用此设备的项目所属类别
    Project	        TEXT(50)	使用此设备的项目名称
    StandardName	TEXT(50)	对应的标准名称
    StandardNumber	TEXT(50)	对应的标准编号
    ClauseNumber	TEXT(50)	对应的条款号
    Equipment   	TEXT(50)	设备的名称
    Manufacturer	TEXT(50)	设备的生产厂家
    Photo	        TEXT(100)	设备照片
    Detail	        TEXT(200)	设备详情
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''
class Equipment(models.Model):

    Category = models.CharField(max_length=50, null=True)
    Project = models.CharField(max_length=50, null=True)
    StandardName = models.CharField(max_length=50, null=True)
    StandardNumber = models.CharField(max_length=50, null=True)
    ClauseNumber = models.CharField(max_length=50, null=True)
    Equipment = models.CharField(max_length=50, null=True)
    Manufacturer = models.CharField(max_length=50, null=True)
    Photo = models.CharField(max_length=50, null=True)
    Detail = models.CharField(max_length=200, null=True)

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='projects2')


    class Meta:
        # 保证以下三元组的唯一性
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'Equipment',
                    'Manufacturer',
                    'Photo',
                ),
                name='UniqueEquipment',
            )
        ]

    def clean(self):
        # 验证以下五元组是否确实对应 Standard 模型中的一行
        try:
            Project.objects.get(
                Category=self.Category,
                Project=self.Project,
                StandardName=self.StandardName,
                StandardNumber=self.StandardNumber,
                ClauseNumber=self.ClauseNumber
            )
        except Project.DoesNotExist:
            raise ValidationError({'Project': 'Project does not exist.'})

    def __str__(self):
        return f"{self.Project} - {self.StandardName} ({self.StandardNumber})"

'''
规程表(Regulation)											
    ID	            INT	        规程在本表中的ID
    Category	    TEXT(50)	使用此设备的项目所属类别
    Project	        TEXT(50)	使用此设备的项目名称
    StandardName	TEXT(50)	对应的标准名称
    StandardNumber	TEXT(50)	对应的标准编号
    ClauseNumber	TEXT(50)	对应的条款号
    Regulation	    TEXT(100)	操作规程文件
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''
class Regulation(models.Model):

    Category = models.CharField(max_length=50, null=True)
    Project = models.CharField(max_length=50, null=True)
    StandardName = models.CharField(max_length=50, null=True)
    StandardNumber = models.CharField(max_length=50, null=True)
    ClauseNumber = models.CharField(max_length=50, null=True)
    Regulation = models.CharField(max_length=100, null=True)

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='projects3')


    def clean(self):
        try:
            Project.objects.get(
                Category=self.Category,
                Project=self.Project,
                StandardName=self.StandardName,
                StandardNumber=self.StandardNumber,
                ClauseNumber=self.ClauseNumber
            )
        except Project.DoesNotExist:
            raise ValidationError({'Project': 'Project does not exist.'})

    def __str__(self):
        return f"{self.Project} - {self.StandardName} ({self.StandardNumber})"
'''
比对测试模型(Comparison)
    ID	            INT	        比对测试在本表中的ID
    Applicant	    TEXT(50)	申请人姓名
    Category	    TEXT(50)	标准所在的具体类别
    Project 	    TEXT(50)	标准所规定的项目的名称
    StandardName	TEXT(50)	标准名称
    StandardNumber	TEXT(50)	标准号
    ClauseNumber	TEXT(50)	标准下的条款号
    StartDate	    DATETIME	比对测试的计划开始时间
    FinishedDate	DATETIME	比对测试的实际完成时间
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''
class Comparison(models.Model):

    Applicant = models.CharField(max_length=50, null=True)
    Category = models.CharField(max_length=50, null=False)
    Project = models.CharField(max_length=50, null=False)
    StandardName = models.CharField(max_length=50, null=False)
    StandardNumber = models.CharField(max_length=50, null=False)
    ClauseNumber = models.CharField(max_length=50, null=False)
    StartDate = models.DateTimeField(null=True)
    FinishedDate = models.DateTimeField(blank=True, null=True)

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='projects4')


    def clean(self):
        if self.FinishedDate is None:
            pass
        else:
            if self.FinishedDate < self.StartDate:
                raise ValidationError({'FinishedDate': 'FinishedDate must be later than StartDate.'})

        try:
            User.objects.get(
                Name=self.Applicant,
            )
        except User.DoesNotExist:
            raise ValidationError({'Applicant': 'User does not exist.'})
        try:
            Project.objects.get(
                Category=self.Category,
                Project=self.Project,
                StandardName=self.StandardName,
                StandardNumber=self.StandardNumber,
                ClauseNumber=self.ClauseNumber
            )
        except Project.DoesNotExist:
            raise ValidationError({'Project': 'Project does not exist.'})

    def __str__(self):
        return f"{self.Project} - {self.StandardName} ({self.StandardNumber})"
'''
样品模型(Sample)
    ID	            INT	        样品在本表中的ID
    Sample	        TEXT(50)	样品的名称
    Specification	TEXT(50)	样品的规格型号
    Manufacture	    TEXT(50)	样品的生产厂家
    BatchNumber	    TEXT(50)	样品所属的批号
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''
class Sample(models.Model):

    Sample = models.CharField(max_length=50, null=True)
    Specification = models.CharField(max_length=50, null=True)
    Manufacturer = models.CharField(max_length=50, null=True)
    BatchNumber = models.CharField(max_length=50, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'Sample',
                    'Specification',
                    'Manufacturer',
                    'BatchNumber'
                ),
                name='UniqueSample',
            )
        ]

    def __str__(self):
        return self

'''
设备采购表(EquipPurchase)											
    ID	            INT	        采购需求在表中的ID
    Submitter	    TEXT(50)	采购需求的申请人
    Category	    TEXT(50)	标准所在的具体类别
    Project 	    TEXT(50)	标准所规定的项目的名称
    StandardName	TEXT(50)	标准名称
    StandardNumber	TEXT(50)	标准号
    ClauseNumber	TEXT(50)	标准下的条款号
    EquipmentName	TEXT(50)	设备的名称
    Manufacturer	TEXT(50)	设备的生产厂家
    Photo	        TEXT(100)	设备照片
    State	        TEXT(50)	采购需求的状态
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''
class EquipPurchase(models.Model):

    Submitter = models.CharField(max_length=50, null=False)
    Category = models.CharField(max_length=50, null=False)
    Project = models.CharField(max_length=50, null=False)
    StandardName = models.CharField(max_length=50, null=False)
    StandardNumber = models.CharField(max_length=50, null=False)
    ClauseNumber = models.CharField(max_length=50, null=False)
    EquipmentName = models.CharField(max_length=50, null=False)
    Manufacturer = models.CharField(max_length=50, null=False)
    Photo = models.CharField(max_length=100, null=False)
    State = models.CharField(max_length=50, null=False, default='Pending')

    #约束
    class Meta:
        #为 State 设置可选值约束
        constraints = [
            models.CheckConstraint(
                check= models.Q(State = 'Pending')|
                       models.Q(State = 'Finished'),
                name='CheckEquipPurchaseState',
            )
        ]

    def clean(self):
        #确保对应申请人在 User 表中存在
        try:
            User.objects.get(
                Name=self.Submitter
            )
        except User.DoesNotExist:
            raise ValidationError({'Submitter': 'User does not exist.'})
        #确保对应标准在标准表中存在
        try:
            Project.objects.get(
                Category=self.Category,
                Project=self.Project,
                StandardName=self.StandardName,
                StandardNumber=self.StandardNumber,
                ClauseNumber=self.ClauseNumber
            )
        except Project.DoesNotExist:
            raise ValidationError({'Project': 'Project does not exist.'})
        #确保对应设备在设备表中存在
        try:
            Equipment.objects.get(
                EquipmentName=self.EquipmentName,
                Manufacturer=self.Manufacturer,
                Photo=self.Photo
            )
        except Equipment.DoesNotExist:
            raise ValidationError({'Equipment': 'Equipment does not exist.'})

    def __str__(self):
        return self

'''
样品采购表(SamplePurchase)
    ID	                INT	        样品采购需求在本表中的ID
    Submitter	        TEXT(50)	样品采购者
    Category	        TEXT(50)	使用此样品的项目所属类别
    Project	            TEXT(50)	使用此样品的项目名称
    StandardName	    TEXT(50)	对应的标准名称
    StandardNumber	    TEXT(50)	对应的标准编号
    ClauseNumber	    TEXT(50)	对应的条款号
    Sample	            TEXT(50)	样品的名称
    Specification	    TEXT(50)	样品的规格型号
    Manufacturer	    TEXT(50)	样品的生产厂家
    BatchNumber	        TEXT(50)	样品所属的批号
    RequiredQuantity	INT	        申请的样品数量
    ActualQuantity	    INT	        实际发放的样品数量
    ApplicationTime	    DATETIME	采购需求的申请时间
    DeliveryTime	    DATETIME	样品发放的时间
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''
class SamplePurchase(models.Model):

    Submitter = models.CharField(max_length=50, null=False)
    Category = models.CharField(max_length=50, null=False)
    Project = models.CharField(max_length=50, null=False)
    StandardName = models.CharField(max_length=50, null=False)
    StandardNumber = models.CharField(max_length=50, null=False)
    ClauseNumber = models.CharField(max_length=50, null=False)
    Sample = models.CharField(max_length=50, null=False)
    Specification = models.CharField(max_length=50, null=False)
    Manufacturer = models.CharField(max_length=50, null=False)
    BatchNumber = models.CharField(max_length=50, null=False)
    RequiredQuantity = models.IntegerField(null=False)
    ActualQuantity = models.IntegerField(null=False)
    ApplicationTime = models.DateTimeField()
    DeliveryTime = models.DateTimeField(blank=True, null=True)

    def clean(self):
        # 确保对应申请人在 User 表中存在
        try:
            User.objects.get(
                Name=self.Submitter
            )
        except User.DoesNotExist:
            raise ValidationError({'Submitter': 'User does not exist.'})
        try:
            Project.objects.get(
                Category=self.Category,
                Project=self.Project,
                StandardName=self.StandardName,
                StandardNumber=self.StandardNumber,
                ClauseNumber=self.ClauseNumber
            )
        except Project.DoesNotExist:
            raise ValidationError({'Project': 'Project does not exist.'})
        try:
            Sample.objects.get(
                Sample=self.Sample,
                Specification=self.Specification,
                Manufacturer=self.Manufacturer,
                BatchNumber=self.BatchNumber
            )
        except Sample.DoesNotExist:
            raise ValidationError({'Sample': 'Sample does not exist.'})

    def __str__(self):
        return self

'''
提醒表(Reminder)											
    ID	            INT	        提醒在本表中的ID
    Submitter	    TEXT(50)	提交提醒的人
    Category	    TEXT(50)	标准所在的具体类别
    Project	        TEXT(50)	标准所规定的项目的名称
    StandardName	TEXT(50)	标准名称
    StandardNumber	TEXT(50)	标准号
    ClauseNumber	TEXT(50)	标准下的条款号
    Staff	        TEXT(200)	模块"人"下的提醒内容
    Equipment	    TEXT(200)	模块"机"下的提醒内容
    Regulation	    TEXT(200)	模块"法"下的提醒内容
    Sample	        TEXT(200)	模块"料"下的提醒内容
    State	        TEXT(20)	该提醒的状态
注:Django默认为数据库表创建'ID'作为主键,无需在模型中进行额外定义
'''
class Reminder(models.Model):

    Submitter = models.CharField(max_length=50, null=False)
    Category = models.CharField(max_length=50, null=False)
    Project = models.CharField(max_length=50, null=False)
    StandardName = models.CharField(max_length=50, null=False)
    StandardNumber = models.CharField(max_length=50, null=False)
    ClauseNumber = models.CharField(max_length=50, null=False)
    Staff = models.CharField(max_length=200, null=False)
    EquipmentName = models.CharField(max_length=200, null=False)
    Regulation = models.CharField(max_length=200, null=False)
    Sample = models.CharField(max_length=200, null=False)
    State = models.CharField(max_length=20, null=False, default='Pending')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check= models.Q(State = 'Pending')|
                       models.Q(State = 'Finished'),
                name='CheckReminderState',
            )
        ]

    def clean(self):
        try:
            User.objects.get(
                Name=self.Submitter
            )
        except User.DoesNotExist:
            raise ValidationError({'Submitter': 'User does not exist.'})
        try:
            Project.objects.get(
                Category=self.Category,
                Project=self.Project,
                StandardName=self.StandardName,
                StandardNumber=self.StandardNumber,
                ClauseNumber=self.ClauseNumber
            )
        except Project.DoesNotExist:
            raise ValidationError({'Project': 'Project does not exist.'})

'''
学习资料表(Tutorial)
    Category	    TEXT(50)	标准所在的具体类别
    Project 	    TEXT(50)	标准所规定的项目的名称
    StandardName	TEXT(50)	标准名称
    StandardNumber	TEXT(50)	标准号
    ClauseNumber	TEXT(50)	标准下的条款号
    Tutorial        FILE        教程文件
'''

class Tutorial(models.Model):
    Category = models.CharField(max_length=50, null=False)
    Project = models.CharField(max_length=50, null=False)
    StandardName = models.CharField(max_length=50, null=False)
    StandardNumber = models.CharField(max_length=50, null=False)
    ClauseNumber = models.CharField(max_length=50, null=False)
    Media = models.FileField(upload_to='Media/', null=True)

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='projects5')

    class Meta:
        constraints = []

    def __str__(self):
        return f"{self.Project} - {self.StandardName} ({self.StandardNumber})"
'''
试卷表(Paper)
    Category	    TEXT(50)	标准所在的具体类别
    Project 	    TEXT(50)	标准所规定的项目的名称
    StandardName	TEXT(50)	标准名称
    StandardNumber	TEXT(50)	标准号
    ClauseNumber	TEXT(50)	标准下的条款号
    Paper           FILE        试卷文件
    Type            TEXT(50)    试卷类型    
'''
class Paper(models.Model):
    Category = models.CharField(max_length=50, null=False)
    Project = models.CharField(max_length=50, null=False)
    StandardName = models.CharField(max_length=50, null=False)
    StandardNumber = models.CharField(max_length=50, null=False)
    ClauseNumber = models.CharField(max_length=50, null=False)

    Paper = models.FileField(upload_to='Papers/')
    Type = models.CharField(max_length=50, null=False)

    project = models.ForeignKey('Project', on_delete=models.CASCADE)



    def __str__(self):
        return f"{self.Project} - {self.StandardName} ({self.StandardNumber})"