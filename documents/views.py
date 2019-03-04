
from myapp.models import Demand, Position
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from documents.models import Documents
from users.models import Profile


@login_required
@permission_required('documents.can_view_create_documents', 'non' )
def documents_list(request, id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	documents = Documents.objects.filter(id_demand=id_demand)
	return render(request, 'documents/documents_list.html',{'documents': documents})


# Создание PDF
@login_required
@permission_required('myapp.can_create_document', 'non')
def create_pdf(request, id_demand, ):
	demand = get_object_or_404(Demand, id=id_demand)
	positions = Position.objects.filter(id_demand=id_demand)

	#	Заявка
	demand_date = "%s" % demand.created_date.strftime('%d.%m.%Y')
	demand_number = "%s" % demand.id
	demand_description = "%s" % demand.description
	demand_quantity_pos = "%s" % demand.position_count()
	demand_quantity_prod = "%s" % demand.product_count()
	demand_price_all = "%s" % demand.price_all()

	today_date = datetime.datetime.today()
	filename =  'Demand_' + str(demand.id) + '_detail' +'.pdf'
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="%s"' % filename

	myfont = ttfonts.TTFont('Times', r'C:\Users\admin\djangopr\myapp\static\myapp\TIMES.TTF')
	pdfmetrics.registerFont(myfont)

	demand_date = demand.created_date.strftime('%d.%m.%Y')
	demand_number = "%s" % demand.id
	demand_description = "%s" % demand.description
	demand_quantity_pos = "%s" % demand.position_count()
	demand_quantity_prod = "%s" % demand.product_count()
	demand_price_all = "%s" % demand.price_all()

	styles = getSampleStyleSheet()
	# temp = BytesIO()

	#   Стили
	style_par = ParagraphStyle("text", fontName="Times",
							   fontSize=12,
							   alignment=TA_LEFT,
							   spaceAfter=5,
							   spaceBefore=5)
	style_nametable = ParagraphStyle("text", fontName="Times",
									 fontSize=14,
									 alignment=TA_CENTER,
									 spaceAfter=15,
									 spaceBefore=30)
	style_title = ParagraphStyle("text", fontName="Times",
								 fontSize=18,
								 alignment=TA_CENTER,
								 spaceAfter=30,
								 spaceBefore=10)

	style_pos_name = ParagraphStyle("text",fontName="Times",
									fontSize=11,
									alignment = TA_CENTER,
									wordWrap=True
									)


	story = [Spacer(1, -0.5 * inch)]

	#   Шапка документа
	header = Paragraph("Информация по заявке №{0}".format(demand_number), style=style_title)
	story.append(header)

	#   Описание заявки
	a = Paragraph("Дата создания: {0}".format(demand_date), style=style_par)
	b = Paragraph("Описание: {0}".format(demand_description), style=style_par)
	c = Paragraph("Кол-во позиций: {0}".format(demand_quantity_pos), style=style_par)
	d = Paragraph("Кол-во товаров: {0}".format(demand_quantity_prod), style=style_par)
	e = Paragraph("Общая ст-ть (руб): {0}".format(demand_price_all), style=style_par)
	story.append(a)
	story.append(b)
	story.append(c)
	story.append(d)
	story.append(e)

	doc2 = SimpleDocTemplate(settings.MEDIA_ROOT + '\\' + today_date.strftime('%Y') + '\\' + today_date.strftime('%m') + '\\' + \
							 filename, rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=30)
	blok_table = []
	title = Paragraph("Позиции в заявке №{0}".format(demand_number), style=style_nametable)
	story.append(title)
	if len(positions) == 0:
		no = Paragraph("Нет созданных позиций для данной заявки", style=style_nametable)
		story.append(no)
	else:
		tablehead = [[u'Наименование товара', u'Артикул товара', u'Кол-во', u'Цена за 1 шт', u'Общая стоимость']]
		tabhead = Table(tablehead, rowHeights=[1 * cm], colWidths=[7.5 * cm, 4 * cm, 1.5 * cm, 3.5 * cm, 3.5 * cm])
		tabhead.setStyle(TableStyle([
			('FONT', (0, 0), (-1, -1), 'Times', 10),
			('ALIGN', (0, 0), (-1, -1), 'CENTER'),
			('GRID', (0, 0), (-1, -1), 0.25, colors.black),
		]))
		story.append(tabhead)
	for position in positions:
		tablebody = [[Paragraph("%s" %position.id_product.name, style=style_pos_name), "%s" % position.id_product.art, "%s" % position.quantity,
			 "%s" % position.id_product.price_one, "%s" % position.cost()]]

		tabbody = Table(tablebody, colWidths=[7.5 * cm, 4 * cm, 1.5 * cm, 3.5 * cm, 3.5 * cm])
		tabbody.setStyle(TableStyle([
			('FONT', (0, 0), (-1, -1), 'Times', 10),
			('ALIGN', (0, 0), (-1, -1), 'CENTER'),
			('GRID', (0, 0), (-1, -1), 0.25, colors.black),
		]))

		story.append(tabbody)

	#   Оформление подвала
	date_created = today_date.strftime("%d.%m.%Y")
	user_created = request.user.last_name + ' ' + request.user.first_name[0] +'. ' + request.user.profile.middle_name[0]
	tablefooter = [[u'Подписи:', u'Дата:      '], [u'{0}'.format(user_created), u'{0}'.format(date_created)]]
	tabfoo = Table(tablefooter, rowHeights=30, colWidths=200, spaceBefore=50)

	tabfoo.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Times', 11), ('ALIGN', (0, 0), (0, -1), 'LEFT'),
								('ALIGN', (1, 0), (1, -1), 'RIGHT'), ]))

	story.append(tabfoo)

	doc2.build(story)
	# f = open('test.pdf', 'w')
	# f.write(str(temp.getpdfdate()))
	# f.close()

	# pdf = temp.getvalue()
	# response.write(pdf)
	# temp.close()

	pdf_url = settings.MEDIA_URL + today_date.strftime('%Y') + '/' + today_date.strftime('%m') + '/' + filename

	Documents.objects.create(date_create=today_date, user_create=Profile.objects.get(id=request.user.id), id_demand=Demand.objects.get(id=id_demand), name_doc=filename, url=pdf_url)

	return HttpResponse(pdf_url)

