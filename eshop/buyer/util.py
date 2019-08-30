from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def itsdangerous_encrypt(data, key, expires):
    """
    itsdangerous加密
    :param data: 加密的数据，字典格式
    :param key: 秘钥
    :param expires: 加密时间
    :return: 加密后的数据，字符串格式
    """
    # 创建加密对象
    myserializer = Serializer(key, expires)
    # 加密
    new_data = myserializer.dumps(data).decode()
    # 返回
    return new_data


def itsdangerous_deencrypt(data, key, expires):
    """
    itsdangerous解密
    :param data: 解密的数据，字符串格式
    :param key: 秘钥
    :param expires: 加密时间
    :return: 解密后的数据，字典格式
    """
    # 创建加密对象
    myserializer = Serializer(key, expires)
    # 解密
    new_data = myserializer.loads(data)
    # 返回
    return new_data
