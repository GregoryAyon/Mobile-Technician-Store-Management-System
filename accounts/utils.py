from datetime import date, timedelta, datetime

def get_weeks():
    current_date = date.today()
    if date.weekday(current_date) == 5:      #if it's Saturday
        current_date = current_date +  timedelta(days=2) # then make it monday
    elif date.weekday(current_date) == 6:      #if it's Sunday
        current_date = current_date +  timedelta(days=1) # then make it monday

    week_start = current_date -  timedelta(days=current_date.weekday()+2)
    week_end = week_start + timedelta(days=7)
    return week_start,week_end
def get_months():
    date_today = datetime.today()
    month_fday = date_today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = date_today.replace(day=28) + timedelta(days=4)
    month_lday = next_month - timedelta(days = next_month.day)
    return month_fday,month_lday

def get_total(orders):
    total_income = 0
    total_service_charge = 0
    total_parts_cost = 0
    total_refreshment_cost = 0
    for order in orders:
        total_service_charge = total_service_charge + order.service_charge
        total_parts_cost = total_parts_cost + order.parts_cost
        total_refreshment_cost = total_refreshment_cost + order.refreshment_cost

    total_income = total_service_charge - (total_parts_cost + total_refreshment_cost)

    return total_income
