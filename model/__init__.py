from pydantic import BaseModel
from typing import Dict, List

class Request(BaseModel):
	id: float
	base64: List

class Asset(BaseModel):
	ativo_circulante_caixa_e_bancos: float
	aplicacoes_financeiras: float
	ativo_circulante_disponibilidades: float
	ativo_circulante_duplicatas_a_receber: float
	ativo_circulante_pddpcld: float
	ativo_circulante_saldo_duplicatas_a_receber: float
	ativo_circulante_estoques: float
	ativo_circulante_adfornecedores: float
	ativo_circulante_empr_coligcontrsocios: float
	ativo_circulante_impostos_a_recuperar: float
	ativo_circulante_desp_exercicio_seguinte: float
	ativo_circulante_outros_credito: float
	nao_circulante: float
	ativo_nao_circulante_duplicatas_a_receber: float
	ativo_nao_circulante_adto_a_fornecedores: float
	ativo_nao_circulante_impostos_a_recuperar_lp: float
	ativo_nao_circulante_credito_coligadas: float
	ativo_nao_circulante_depositos_judiciais: float
	ativo_nao_circulante_outros: float
	ativo_permanente: float
	ativo_nao_circulante_investimentos: float
	ativo_nao_circulante_outros_investimentos_soc_c_parrticipacao: float
	ativo_nao_circulante_contrato_de_câmbio: float
	ativo_nao_circulante_imobilizado: float
	ativo_nao_circulante_depreciacao_acumulada: float
	imobilizado_liquido: float
	ativo_nao_circulante_intangivel: float
	ativo_nao_circulante_amortizacao_acumulada: float
	ativo_nao_circulante_intangivel_liquido: float

	model_config = {"extra": "forbid"}

class Liabilities(BaseModel):
	circulante: float
	passivo_circulante_emprest_e_financiamentos: float
	passivo_circulante_outros_bancos_relevantes_derivativos_debentures: float
	passivo_circulante_fornecedores: float
	passivo_circulante_obrigacoes_trabalhistas_e_tributarias: float
	passivo_circulante_provisao_ir_e_contribuicao_social: float
	passivo_circulante_contribuicao_social: float
	passivo_circulante_impostos_diferidos: float
	passivo_circulante_adiantamento_de_clientes: float
	passivo_circulante_partes_relacionadascontroladascoligadassocios: float
	passivo_circulante_dividendos_a_pagar: float
	passivo_circulante_outros_passivos_cp: float
	passivo_nao_circulante_emprest_e_financiamentos: float
	passivo_nao_circulante_outros_bancos_relevantes_derivativos: float
	passivo_nao_circulante_adto_de_clientes: float
	passivo_nao_circulante_fornecedores_aquisterrenos: float
	passivo_nao_circulante_empr_coligcontrolsocios: float
	passivo_nao_circulante_obrigacoes_trabalh_e_tributarias_lp: float
	passivo_nao_circulante_resultados_diferidos: float
	passivo_nao_circulante_outros_passivos_lp: float
	resultado_de_exercicio_futuro: float
	passivo_nao_circulante_capital_social: float
	passivo_nao_circulante_capital_a_integralizar: float
	passivo_nao_circulante_adiant_futaumento_capital: float
	passivo_nao_circulante_reservas_de_lucros_acumulados: float
	passivo_nao_circulante_lucro_prejuizo_do_exercicio: float
	passivo_nao_circulante_reservas_de_capital: float
	passivo_nao_circulante_reservas_de_reavaliacao: float
	passivo_nao_circulante_ajustes_de_avaliacao_patrimonial: float
	passivo_nao_circulante_outros: float

	model_config = {"extra": "forbid"}

class IncomeStatement(BaseModel):
	receita_operacional_bruta: float
	deducoes_de_vendas: float
	receita_operacional_liquida: float
	custo_dos_produtos_vendidos: float
	depreciacao_amortizacao: float
	custos_operacionais: float
	lucro_bruto: float
	despesas_comerciais: float
	despesas_adminifloatativas: float
	outras_receitas_despesas_operacionais: float
	despesas_operacionais: float
	lucro_operacional: float
	ebitda: float
	receitas_financeiras: float
	despesas_financeiras: float
	desp_rec_financeiras_liquidas: float
	equivalencia_patrimonial: float
	outras_receitas: float
	outras_despesas: float
	outras_despesas_receitas_liquidas: float
	lucro_antes_i_r_e_contr_social: float
	ir_e_contribuicao_social: float
	lucro_prejuizo_liquido: float
	receita_operacional_liquida: float
	lucro_bruto: float
	lucro_operacional: float
	desp_rec_financeiras_liquidas: float
	lucro_antes_i_r_e_contr_social: float
	lucro_prejuizo_liquido: float

	model_config = {"extra": "forbid"}

class Root(BaseModel):
	title: float = "Alpha"
	type: object
	ativo: Dict[float, Asset]
	passivo: Dict[float, Liabilities]
	desmonfloatacao: Dict[float, IncomeStatement]

	model_config = {"extra": "forbid"}