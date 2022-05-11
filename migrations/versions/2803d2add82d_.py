"""empty message

Revision ID: 2803d2add82d
Revises: 
Create Date: 2022-05-10 23:35:05.230740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2803d2add82d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('AdminId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('AdminEmail', sa.String(length=100), nullable=False),
    sa.Column('AdminName', sa.String(length=200), nullable=False),
    sa.Column('AdminPassword', sa.String(length=200), nullable=False),
    sa.Column('AdminSex', sa.Boolean(), nullable=True),
    sa.Column('AdminJoin_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('AdminId'),
    sa.UniqueConstraint('AdminEmail'),
    sa.UniqueConstraint('AdminName')
    )
    op.create_table('email_captcha',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('captcha', sa.String(length=10), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user',
    sa.Column('UserId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('UserEmail', sa.String(length=100), nullable=False),
    sa.Column('UserName', sa.String(length=200), nullable=False),
    sa.Column('UserIdcard', sa.String(length=18), nullable=True),
    sa.Column('UserSex', sa.Boolean(), nullable=True),
    sa.Column('UserAddress', sa.String(length=200), nullable=True),
    sa.Column('UserPhone', sa.String(length=20), nullable=True),
    sa.Column('UserPassword', sa.String(length=200), nullable=False),
    sa.Column('UserCredit', sa.Integer(), nullable=True),
    sa.Column('UserJoin_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('UserId'),
    sa.UniqueConstraint('UserEmail'),
    sa.UniqueConstraint('UserIdcard'),
    sa.UniqueConstraint('UserName')
    )
    op.create_table('goods',
    sa.Column('GoodsId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('GoodsPrice', sa.Float(), nullable=False),
    sa.Column('GoodsStock', sa.Integer(), nullable=False),
    sa.Column('GoodsDescribe', sa.String(length=1024), nullable=False),
    sa.Column('GoodsTime', sa.DateTime(), nullable=True),
    sa.Column('UserId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['UserId'], ['user.UserId'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('GoodsId')
    )
    op.create_table('comment',
    sa.Column('CommentId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('CommentDescribe', sa.String(length=1024), nullable=False),
    sa.Column('CommentTime', sa.DateTime(), nullable=True),
    sa.Column('UserId', sa.Integer(), nullable=True),
    sa.Column('GoodsId', sa.Integer(), nullable=True),
    sa.Column('CommentReply', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CommentReply'], ['comment.CommentId'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['GoodsId'], ['goods.GoodsId'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['UserId'], ['user.UserId'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('CommentId')
    )
    op.create_table('order',
    sa.Column('OrderId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('OrderExpress', sa.String(length=200), nullable=True),
    sa.Column('OrderNum', sa.Integer(), nullable=False),
    sa.Column('OrderAddress', sa.String(length=200), nullable=False),
    sa.Column('OrderPhone', sa.String(length=11), nullable=False),
    sa.Column('OrderTime', sa.DateTime(), nullable=True),
    sa.Column('OrderIsfinished', sa.Boolean(), nullable=True),
    sa.Column('UserId', sa.Integer(), nullable=True),
    sa.Column('GoodsId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['GoodsId'], ['goods.GoodsId'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['UserId'], ['user.UserId'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('OrderId'),
    sa.UniqueConstraint('OrderExpress')
    )
    op.create_table('evaluation',
    sa.Column('EvaluationId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('EvaluationDescribe', sa.String(length=1024), nullable=False),
    sa.Column('EvaluationPicture', sa.BLOB(), nullable=True),
    sa.Column('EvaluationScore', sa.Integer(), nullable=True),
    sa.Column('EvaluationTime', sa.DateTime(), nullable=True),
    sa.Column('OrderId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['OrderId'], ['order.OrderId'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('EvaluationId')
    )
    op.create_table('return',
    sa.Column('ReturnId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ReturnAddress', sa.String(length=200), nullable=False),
    sa.Column('ReturnReason', sa.String(length=200), nullable=False),
    sa.Column('ReturnTime', sa.DateTime(), nullable=True),
    sa.Column('ReturnExpress', sa.String(length=200), nullable=True),
    sa.Column('ReturnIsfinished', sa.Boolean(), nullable=True),
    sa.Column('UserId', sa.Integer(), nullable=True),
    sa.Column('OrderId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['OrderId'], ['order.OrderId'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['UserId'], ['user.UserId'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('ReturnId'),
    sa.UniqueConstraint('ReturnExpress')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('return')
    op.drop_table('evaluation')
    op.drop_table('order')
    op.drop_table('comment')
    op.drop_table('goods')
    op.drop_table('user')
    op.drop_table('email_captcha')
    op.drop_table('admin')
    # ### end Alembic commands ###