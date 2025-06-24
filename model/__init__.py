from pydantic import BaseModel
from typing import Dict, List

class Request(BaseModel):
	id: str
	base64: List

class Ativo(BaseModel):
	ativo_circulante_caixa_e_bancos: str
	aplicacoes_financeiras: str
	ativo_circulante_disponibilidades: str
	ativo_circulante_duplicatas_a_receber: str
	ativo_circulante_pddpcld: str
	ativo_circulante_saldo_duplicatas_a_receber: str
	ativo_circulante_estoques: str
	ativo_circulante_adfornecedores: str
	ativo_circulante_empr_coligcontrsocios: str
	ativo_circulante_impostos_a_recuperar: str
	ativo_circulante_desp_exercicio_seguinte: str
	ativo_circulante_outros_credito: str
	nao_circulante: str
	ativo_nao_circulante_duplicatas_a_receber: str
	ativo_nao_circulante_adto_a_fornecedores: str
	ativo_nao_circulante_impostos_a_recuperar_lp: str
	ativo_nao_circulante_credito_coligadas: str
	ativo_nao_circulante_depositos_judiciais: str
	ativo_nao_circulante_outros: str
	ativo_permanente: str
	ativo_nao_circulante_investimentos: str
	ativo_nao_circulante_outros_investimentos_soc_c_parrticipacao: str
	ativo_nao_circulante_contrato_de_câmbio: str
	ativo_nao_circulante_imobilizado: str
	ativo_nao_circulante_depreciacao_acumulada: str
	imobilizado_liquido: str
	ativo_nao_circulante_intangivel: str
	ativo_nao_circulante_amortizacao_acumulada: str
	ativo_nao_circulante_intangivel_liquido: str

	model_config = {"extra": "forbid"}

class Passivo(BaseModel):
	circulante: str
	passivo_circulante_emprest_e_financiamentos: str
	passivo_circulante_outros_bancos_relevantes_derivativos_debentures: str
	passivo_circulante_fornecedores: str
	passivo_circulante_obrigacoes_trabalhistas_e_tributarias: str
	passivo_circulante_provisao_ir_e_contribuicao_social: str
	passivo_circulante_contribuicao_social: str
	passivo_circulante_impostos_diferidos: str
	passivo_circulante_adiantamento_de_clientes: str
	passivo_circulante_partes_relacionadascontroladascoligadassocios: str
	passivo_circulante_dividendos_a_pagar: str
	passivo_circulante_outros_passivos_cp: str
	passivo_nao_circulante_emprest_e_financiamentos: str
	passivo_nao_circulante_outros_bancos_relevantes_derivativos: str
	passivo_nao_circulante_adto_de_clientes: str
	passivo_nao_circulante_fornecedores_aquisterrenos: str
	passivo_nao_circulante_empr_coligcontrolsocios: str
	passivo_nao_circulante_obrigacoes_trabalh_e_tributarias_lp: str
	passivo_nao_circulante_resultados_diferidos: str
	passivo_nao_circulante_outros_passivos_lp: str
	resultado_de_exercicio_futuro: str
	passivo_nao_circulante_capital_social: str
	passivo_nao_circulante_capital_a_integralizar: str
	passivo_nao_circulante_adiant_futaumento_capital: str
	passivo_nao_circulante_reservas_de_lucros_acumulados: str
	passivo_nao_circulante_lucro_prejuizo_do_exercicio: str
	passivo_nao_circulante_reservas_de_capital: str
	passivo_nao_circulante_reservas_de_reavaliacao: str
	passivo_nao_circulante_ajustes_de_avaliacao_patrimonial: str
	passivo_nao_circulante_outros: str

	model_config = {"extra": "forbid"}

class DemonstracaoResultadoExercicio(BaseModel):
	receita_operacional_bruta: str
	deducoes_de_vendas: str
	receita_operacional_liquida: str
	custo_dos_produtos_vendidos: str
	depreciacao_amortizacao: str
	custos_operacionais: str
	lucro_bruto: str
	despesas_comerciais: str
	despesas_administrativas: str
	outras_receitas_despesas_operacionais: str
	despesas_operacionais: str
	lucro_operacional: str
	ebitda: str
	receitas_financeiras: str
	despesas_financeiras: str
	desp_rec_financeiras_liquidas: str
	equivalencia_patrimonial: str
	outras_receitas: str
	outras_despesas: str
	outras_despesas_receitas_liquidas: str
	lucro_antes_i_r_e_contr_social: str
	ir_e_contribuicao_social: str
	lucro_prejuizo_liquido: str
	receita_operacional_liquida: str
	lucro_bruto: str
	lucro_operacional: str
	desp_rec_financeiras_liquidas: str
	lucro_antes_i_r_e_contr_social: str
	lucro_prejuizo_liquido: str

	model_config = {"extra": "forbid"}

class Root(BaseModel):
	title: str = "Alpha"
	type: object
	ativo: Dict[str, Ativo]
	passivo: Dict[str, Passivo]
	desmonstracao: Dict[str, DemonstracaoResultadoExercicio]

	model_config = {"extra": "forbid"}