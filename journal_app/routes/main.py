from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask_mail import Message
from datetime import datetime
import smtplib

from journal_app.settings import (mail_username, mail_password, mail_server,
                                  mail_port, mail_receipt)
from journal_app.extensions import db, mail
from journal_app.models import Entry, User, EntryForm, ContactForm

main = Blueprint('main', __name__)


@main.route('/about', methods=['GET', 'POST'])
def about():
    form = ContactForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.aboutus'))
    if form.validate_on_submit():
        fromAddr = mail_username
        toAddr = mail_receipt
        userEmail = form.email.data
        name = form.name.data
        subject = form.subject.data
        body = form.body.data

        msg = """Name: %s\nEmail: %s\nSubject: %s\n\n%s
        """ % (name, ", ".join(userEmail), subject, body)

        server = smtplib.SMTP(mail_server, mail_port)
        server.ehlo()
        server.starttls()
        server.login(mail_username, mail_password)
        server.sendmail(fromAddr, toAddr, msg)
        server.close()
        # with mail.connect() as conn:
        #     msg = Message(form.subject.data,
        #                   sender='contact500words@gmail.com',
        #                   recipients=['lyndi321@gmail.com'])
        #     msg.body = """
        #     From: %s &lt;%s&gt;
        #     %s
        #     """ % (form.name.data, form.email.data, form.body.data)
        #     conn.send(msg)

        return render_template('about.html', success=True)
    return render_template('about.html', form=form)


@main.route('/aboutus')
@login_required
def aboutus():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(form.subject.data,
                      sender='contact500words@gmail.com',
                      recipients=['lyndi321@gmail.com'])
        msg.body = """
        From: %s &lt;%s&gt;
        %s
        """ % (form.name.data, form.email.data, form.body.data)
        mail.send(msg)

        return render_template('aboutus.html', success=True)
    return render_template('aboutus.html',
                           form=form,
                           name=current_user.name,
                           email=current_user.email)


@main.route('/dashboard')
@login_required
def dashboard():
    entries = Entry.query.all()

    return render_template('dashboard.html',
                           name=current_user.name,
                           entries=entries)


@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = EntryForm()

    if form.validate_on_submit():
        new_entry = Entry(title=form.title.data,
                          content=form.content.data,
                          word_count=request.form['totalCount'],
                          date_submitted=str(
                              datetime.utcnow().strftime('%Y-%m-%d')))
        new_entry.user = current_user
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('write.html', form=form)


@main.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = EntryForm()
    entry = Entry.query.get(id)
    form.title.data = entry.title
    form.content.data = entry.content
    form.word_count.data = entry.word_count
    db.session.rollback()

    if request.method == 'POST' and form.validate_on_submit():
        totalCount = request.form['totalCount']
        if totalCount != '':
            entry.word_count = totalCount
        entry.title = request.form['title']
        entry.content = request.form['content']
        entry.date_submitted = str(datetime.utcnow().strftime('%Y-%m-%d'))
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('edit.html', form=form, id=id)


@main.route('/delete/<string:id>', methods=['GET'])
@login_required
def delete(id):
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('main.dashboard'))
