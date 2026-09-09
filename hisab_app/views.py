# Updated Django Views with better error handling

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse

from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet


from .models import Person, Hisab
from .serializers import PersonSerializer, HisabSerializer

@api_view(['GET', 'POST'])
def person_list_create(request):
    if request.method == 'GET':
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def person_hisabs(request, pk):
    try:
        person = get_object_or_404(Person, pk=pk)
        hisabs = person.hisabs.all()
        serializer = HisabSerializer(hisabs, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
def person_detail(request, pk):
    try:
        person = get_object_or_404(Person, pk=pk)
        
        if request.method == 'GET':
            serializer = PersonSerializer(person)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = PersonSerializer(person, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            person.delete()
            return Response({"message": "Person deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['DELETE'])
# def delete_person(request, pk):
#     try:
#         person = get_object_or_404(Person, pk=pk)
#         person.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def hisab_list_create(request):
    if request.method == 'GET':
        hisabs = Hisab.objects.all()
        serializer = HisabSerializer(hisabs, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = HisabSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def hisab_detail(request, pk):
    try:
        hisab = get_object_or_404(Hisab, pk=pk)
        
        if request.method == 'GET':
            serializer = HisabSerializer(hisab)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = HisabSerializer(hisab, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            hisab.delete()
            return Response({"message": "Hisab deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_hisab(request, pk):
    try:
        hisab = get_object_or_404(Hisab, pk=pk)
        hisab.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# PDF Generation View
@api_view(['POST'])
def generate_hisab_pdf(request):
    try:
        # Get data from request
        hisabs_data = request.data.get('hisabs', [])
        start_date = request.data.get('startDate')
        end_date = request.data.get('endDate')
        person_name = request.data.get('personName', '')
        
        # Create PDF buffer
        buffer = BytesIO()
        
        # Create PDF document with better margin
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles["Heading1"]
        title_style.alignment = 1  # Center alignment
        title_style.textColor = colors.darkblue
        
        subtitle_style = styles["Heading2"]
        subtitle_style.alignment = 1  # Center alignment
        subtitle_style.textColor = colors.darkblue
        subtitle_style.spaceAfter = 12
        
        date_style = styles["Normal"]
        date_style.alignment = 1  # Center alignment
        date_style.fontName = 'Helvetica-Oblique'
        date_style.fontSize = 10
        date_style.textColor = colors.darkslategray
        date_style.spaceAfter = 20
        
        normal_style = styles["Normal"]
        normal_style.fontSize = 10
        normal_style.spaceAfter = 6
        
        # Create document elements
        elements = []
        
        # Add logo/header image if available
        # elements.append(Image('path/to/logo.png', width=200, height=50))
        # elements.append(Spacer(1, 20))
        
        # Add title and subtitle
        elements.append(Paragraph(f"Hisab Report", title_style))
        elements.append(Paragraph(f"for {person_name}", subtitle_style))
        elements.append(Paragraph(f"Period: {start_date} to {end_date}", date_style))
        
        # Add summary information
        total_amount = sum(float(hisab['price']) for hisab in hisabs_data)
        # online_amount = sum(float(hisab['price']) for hisab in hisabs_data if hisab.get('if_online', False))
        # cash_amount = total_amount - online_amount
        
        # Create summary table
        summary_data = [
            ['Summary', ''],
            ['Total Transactions', f"{len(hisabs_data)}"],
            ['Total Amount', f"Rs {total_amount:.2f}"],
        ]
        
        
        summary_table = Table(summary_data, colWidths=[150, 150])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.darkblue),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (1, 0), 12),
            ('SPAN', (0, 0), (1, 0)),  # Merge the header row
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),  # Right-align the values
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Add transaction details heading
        elements.append(Paragraph("Transaction Details", subtitle_style))
        
        # Group transactions by month
        transactions_by_month = {}
        for hisab in hisabs_data:
            date_obj = datetime.strptime(hisab['date'], '%Y-%m-%d')
            month_key = date_obj.strftime('%B %Y')  # Month name and year
            
            if month_key not in transactions_by_month:
                transactions_by_month[month_key] = []
                
            transactions_by_month[month_key].append(hisab)
        
        # Sort months chronologically
        sorted_months = sorted(transactions_by_month.keys(), 
                               key=lambda x: datetime.strptime(x, '%B %Y'))
        
        # Process each month
        for month in sorted_months:
            month_hisabs = transactions_by_month[month]
            
            # Add month header
            month_style = styles["Heading3"]
            month_style.textColor = colors.darkblue
            elements.append(Paragraph(month, month_style))
            
            # Create month table data
            table_data = [['Date', 'Item', 'Description', 'Amount']]
            
            month_total = 0
            for hisab in month_hisabs:
                date_obj = datetime.strptime(hisab['date'], '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d %b')
                
                # Get transaction type (online/cash)
                trans_type = 'Online' if hisab.get('if_online', False) else 'Cash'
                platform = hisab.get('platform', '')
                if platform and trans_type == 'Online':
                    trans_type = f"{trans_type} ({platform})"
                
                table_data.append([
                    formatted_date,
                    hisab['item'],
                    hisab.get('description', ''),
                    f"Rs {float(hisab['price']):.2f}"
                ])
                
                month_total += float(hisab['price'])
            
            # Add month total row
            table_data.append(['', '', '', 'Month Total:', f"Rs {month_total:.2f}"])
            
            # Create the table
            col_widths = [50, 120, 160, 80, 80]
            month_table = Table(table_data, colWidths=col_widths)
            
            # Define table style
            month_table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                
                # Alternating row colors
                ('BACKGROUND', (0, 1), (-1, -2), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -2), colors.black),
                
                # Total row
                ('BACKGROUND', (0, -1), (-1, -1), colors.whitesmoke),
                ('TEXTCOLOR', (3, -1), (-1, -1), colors.darkblue),
                ('FONTNAME', (3, -1), (-1, -1), 'Helvetica-Bold'),
                ('TOPPADDING', (0, -1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, -1), (-1, -1), 6),
                
                # Common settings
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),  # Right align amounts
                ('ALIGN', (0, 1), (0, -2), 'CENTER'),  # Center align dates
            ]))
            
            elements.append(month_table)
            elements.append(Spacer(1, 15))
        
        # Final note
        note_style = styles["Italic"]
        note_style.alignment = 1  # Center
        note_style.fontSize = 8
        note_style.textColor = colors.grey
        
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("Generated on " + datetime.now().strftime("%d %b %Y, %H:%M:%S"), note_style))
        
        # Build the PDF
        doc.build(elements)
        
        # Get PDF content
        buffer.seek(0)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        # Create response
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Hisab_Report_{person_name}.pdf"'
        return response
        
    except Exception as e:
        return Response(
            {"error": f"PDF generation failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )