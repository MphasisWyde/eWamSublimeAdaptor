# -*- coding: utf-8 -*-
import logging

from bravado_core.param import Param

log = logging.getLogger(__name__)


class Operation(object):
    """Swagger operation defined by a unique (http_method, path_name) pair.

    :type swagger_spec: :class:`Spec`
    :param path_name: path of the operation. e.g. /pet/{petId}
    :param http_method: get/put/post/delete/etc
    :param op_spec: operation specification in dict form
    """
    def __init__(self, swagger_spec, path_name, http_method, op_spec):
        self.swagger_spec = swagger_spec
        self.path_name = path_name
        self.http_method = http_method
        self.op_spec = swagger_spec.deref(op_spec)

        # generated by @property when necessary since this is optional.
        # Diverges from op_* naming scheme since it is called 'operation_id'
        # in the Swagger 2.0 Spec.
        self._operation_id = None

        # (key, value) = (param name, Param)
        self.params = {}

    @property
    def consumes(self):
        """Note that the operation can override the value defined globally
        at #/consumes.

        :return: List of supported mime types consumed by this operation. e.g.
            ["application/x-www-form-urlencoded"]
        :rtype: list of strings, never None
        """
        deref = self.swagger_spec.deref
        result = deref(self.op_spec.get('consumes'))
        if result is None:
            result = deref(self.swagger_spec.spec_dict.get('consumes', []))
        return result

    @property
    def produces(self):
        """Note that the operation can override the value defined globally
        at #/produces.

        :return: List of supported mime types produced by this operation. e.g.
            ["application/json"]
        :rtype: list of strings, never None
        """
        deref = self.swagger_spec.deref
        result = deref(self.op_spec.get('produces'))
        if result is None:
            return deref(self.swagger_spec.spec_dict.get('produces', []))
        return result

    @classmethod
    def from_spec(cls, swagger_spec, path_name, http_method, op_spec):
        """
        Creates a :class:`Operation` and builds up its list of :class:`Param` s

        :param swagger_spec: :class:`Spec`
        :param path_name: path of the operation. e.g. /pet/{petId}
        :param http_method: get/put/post/delete/etc
        :param op_spec: operation specification in dict form
        :rtype: :class:`Operation`
        """
        op = cls(swagger_spec, path_name, http_method, op_spec)
        op.params = build_params(op)
        return op

    @property
    def operation_id(self):
        """A friendly name for the operation. The id MUST be unique among all
        operations described in the API. Tools and libraries MAY use the
        operation id to uniquely identify an operation.

        This this field is not required, it will be generated when needed.

        :rtype: str
        """
        if self._operation_id is None:
            deref = self.swagger_spec.deref
            self._operation_id = deref(self.op_spec.get('operationId'))
            if self._operation_id is None:
                # build based on the http method and request path
                self._operation_id = (self.http_method + '_' + self.path_name)\
                    .replace('/', '_')\
                    .replace('{', '_')\
                    .replace('}', '_')\
                    .replace('__', '_')\
                    .strip('_')
        return self._operation_id

    def __repr__(self):
        return u"%s(%s)" % (self.__class__.__name__, self.operation_id)


def build_params(op):
    """Builds up the list of this operation's parameters taking into account
    parameters that may be available for this operation's path component.

    :type op: :class:`bravado_core.operation.Operation`

    :returns: dict where (k,v) is (param_name, Param)
    """
    swagger_spec = op.swagger_spec
    deref = swagger_spec.deref
    op_spec = deref(op.op_spec)
    op_params_spec = deref(op_spec.get('parameters', []))
    spec_dict = deref(swagger_spec.spec_dict)
    paths_spec = deref(spec_dict.get('paths', {}))
    path_spec = deref(paths_spec.get(op.path_name))
    path_params_spec = deref(path_spec.get('parameters', []))

    # Order of addition is *important* here. Since op_params are last in the
    # list, they will replace any previously defined path_params with the
    # same name when the final params dict is constructed in the loop below.
    params_spec = path_params_spec + op_params_spec

    params = {}
    for param_spec in params_spec:
        param = Param(swagger_spec, op, deref(param_spec))
        params[param.name] = param
    return params