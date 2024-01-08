# coding=utf-8

class RET:
    OK                  = 0

    PWDERR              = 4001
    IPERR               = 4002
    SESSIONERR          = 4003
    REQERR              = 4004
    LIMITERR            = 4005
    PERMISSIONERR       = 4006
    TOKENERR            = 4007

    PARAMERR            = 4101
    TOKEN_OVERFLOW      = 4102

    NODATA              = 4201
    FILEGETERR          = 4202
    DATAERR             = 4203
    IOERR               = 4204

    TASKNOTEXIST        = 4301
    TASKERR             = 4302

    DBERR               = 4501
    SERVERERR           = 4502
    UNKOWNERR           = 4503


error_map = {
    RET.OK              : u"成功",

    RET.PWDERR          : u"密码错误",
    RET.IPERR           : u"IP受限",
    RET.SESSIONERR      : u"用户未登录",
    RET.REQERR          : u"非法请求",
    RET.LIMITERR        : u"接口调用次数受限",
    RET.PERMISSIONERR   : u"权限错误",
    RET.TOKENERR        : u"token错误",

    RET.PARAMERR        : u"参数错误",
    RET.TOKEN_OVERFLOW: u"token长度超过限制",

    RET.NODATA          : u"无数据",
    RET.FILEGETERR      : u"文件获取失败",
    RET.DATAERR         : u"数据错误",
    RET.IOERR           : u"文件读写错误",

    RET.TASKNOTEXIST    : u"任务不存在或已删除",
    RET.TASKERR         : u"任务失败",

    RET.DBERR           : u"数据库错误",
    RET.SERVERERR       : u"服务繁忙, 请稍后重试",
    RET.UNKOWNERR       : u"未知错误"
}

