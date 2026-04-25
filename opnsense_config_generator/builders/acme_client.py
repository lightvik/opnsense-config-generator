from lxml import etree

from opnsense_config_generator.builders.base import append_if, bool_val
from opnsense_config_generator.models.acme_client import (
    AcmeAccount,
    AcmeAction,
    AcmeCertificate,
    AcmeClientConfig,
    AcmeValidation,
)
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def _account_uuid(name: str) -> str:
    return make_uuid("acme_client:account", name)


def _cert_uuid(name: str) -> str:
    return make_uuid("acme_client:certificate", name)


def _validation_uuid(name: str) -> str:
    return make_uuid("acme_client:validation", name)


def _action_uuid(name: str) -> str:
    return make_uuid("acme_client:action", name)


def _build_account(parent: etree._Element, account: AcmeAccount) -> None:
    el = etree.SubElement(parent, "account", uuid=_account_uuid(account.name))
    sub(el, "enabled", bool_val(account.enabled))
    sub(el, "name", account.name)
    append_if(el, "description", account.description or None)
    append_if(el, "email", account.email or None)
    sub(el, "ca", account.ca)
    append_if(el, "custom_ca", account.custom_ca or None)
    append_if(el, "eab_kid", account.eab_kid or None)
    append_if(el, "eab_hmac", account.eab_hmac or None)


def _build_certificate(parent: etree._Element, cert: AcmeCertificate) -> None:
    el = etree.SubElement(parent, "certificate", uuid=_cert_uuid(cert.name))
    sub(el, "enabled", bool_val(cert.enabled))
    sub(el, "name", cert.name)
    append_if(el, "description", cert.description or None)
    if cert.alt_names:
        sub(el, "altNames", ",".join(cert.alt_names))
    sub(el, "account", _account_uuid(cert.account))
    sub(el, "validationMethod", _validation_uuid(cert.validation_method))
    sub(el, "keyLength", cert.key_length)
    sub(el, "ocsp", bool_val(cert.ocsp))
    if cert.restart_actions:
        sub(el, "restartActions", ",".join(_action_uuid(a) for a in cert.restart_actions))
    sub(el, "autoRenewal", bool_val(cert.auto_renewal))
    sub(el, "renewInterval", str(cert.renew_interval))
    sub(el, "aliasmode", cert.aliasmode)
    append_if(el, "domainalias", cert.domain_alias or None)
    append_if(el, "challengealias", cert.challenge_alias or None)


def _build_validation(parent: etree._Element, validation: AcmeValidation) -> None:
    el = etree.SubElement(parent, "validation", uuid=_validation_uuid(validation.name))
    sub(el, "enabled", bool_val(validation.enabled))
    sub(el, "name", validation.name)
    append_if(el, "description", validation.description or None)
    sub(el, "method", validation.method)
    sub(el, "dns_service", validation.dns_service)
    sub(el, "dns_sleep", str(validation.dns_sleep))
    for key, val in validation.dns_credentials.items():
        sub(el, key, val)


def _build_action(parent: etree._Element, action: AcmeAction) -> None:
    el = etree.SubElement(parent, "action", uuid=_action_uuid(action.name))
    sub(el, "enabled", bool_val(action.enabled))
    sub(el, "name", action.name)
    append_if(el, "description", action.description or None)
    sub(el, "type", action.type)
    for key, val in action.extra_params.items():
        sub(el, key, val)


def build_acme_client(cfg: AcmeClientConfig) -> etree._Element | None:
    if (
        not cfg.settings.enabled
        and not cfg.accounts
        and not cfg.certificates
        and not cfg.validations
        and not cfg.actions
    ):
        return None

    el = etree.Element("AcmeClient")

    settings_el = etree.SubElement(el, "settings")
    sub(settings_el, "enabled", bool_val(cfg.settings.enabled))
    sub(settings_el, "autoRenewal", bool_val(cfg.settings.auto_renewal))
    sub(settings_el, "environment", cfg.settings.environment)
    sub(settings_el, "challengePort", str(cfg.settings.challenge_port))
    sub(settings_el, "TLSchallengePort", str(cfg.settings.tls_challenge_port))
    sub(settings_el, "restartTimeout", str(cfg.settings.restart_timeout))
    sub(settings_el, "logLevel", cfg.settings.log_level)

    accounts_el = etree.SubElement(el, "accounts")
    for account in cfg.accounts:
        _build_account(accounts_el, account)

    certs_el = etree.SubElement(el, "certificates")
    for cert in cfg.certificates:
        _build_certificate(certs_el, cert)

    validations_el = etree.SubElement(el, "validations")
    for validation in cfg.validations:
        _build_validation(validations_el, validation)

    actions_el = etree.SubElement(el, "actions")
    for action in cfg.actions:
        _build_action(actions_el, action)

    return el
